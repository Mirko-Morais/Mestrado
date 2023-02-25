'''
Predições Ceará
'''
from pandas import read_sql_query
from numpy import arange
from sklearn.externals import joblib
from etl.database import Vertica
from etl.database import Datawarehouse
from etl.sql_queries import hidrometros_producao_quantidade
from etl.sql_queries import hidrometros_producao_medicoes
from pipelinePandas import pipeline_from_producao
from pipelineSkLearn import predicao_producao


VERTICA = Vertica()
DW = Datawarehouse()
SCALER = joblib.load('./model/scaler_treinado.cagece') #StandardScaler()
MODELO = joblib.load('./model/modelo_treinado.cagece')
QTD_HIDROMETROS_ATIVOS = read_sql_query(hidrometros_producao_quantidade, \
  VERTICA.get_engine()).values[0][0]
LISTA_OFFSETS = arange(0, QTD_HIDROMETROS_ATIVOS, 40000)
SQL_QUERY_LISTA = [hidrometros_producao_medicoes.format(offset) for offset in LISTA_OFFSETS]

def processa_previsoes(consulta, db_instance, schema, modelo=MODELO, scaler=SCALER):
    '''
    dada um determinado dataset processa previsoes com modelo recebido
    '''
    df_consulta = read_sql_query(consulta, db_instance.get_engine())
    df_consulta = pipeline_from_producao(df_consulta)
    df_consulta, predicao, probabilidade = predicao_producao(df_consulta, modelo, scaler)
    df_consulta['predicao'] = predicao
    df_consulta['proba_0'] = probabilidade[:, 0]
    df_consulta['proba_1'] = probabilidade[:, 1]
    df_consulta.to_sql('hid_prd_predicoes_modelo', db_instance.get_engine(), \
      schema=schema, if_exists='append')


NUMERO_INTERACAO = 1
for query in SQL_QUERY_LISTA:
    processa_previsoes(query, VERTICA, 'tmp')
    print('Interação nro ', NUMERO_INTERACAO, ' concluida com sucesso')
    NUMERO_INTERACAO += 1
