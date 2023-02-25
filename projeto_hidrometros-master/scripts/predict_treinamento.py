'''
Classe para previsão do dataset das bancadas.
'''
from pandas import read_sql_query
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from etl.database import Datawarehouse
from etl.sql_queries import hidrometros_bancada_medicoes
from etl.sql_queries import analise_bancada_completa
from pipelinePandas import pipeline_from_bancada_completa
from pipelineSkLearn import predicao_treino


DW = Datawarehouse()
SCALER = StandardScaler()
RFC = RandomForestClassifier(bootstrap=True, criterion='entropy', max_depth=8,\
 max_features='sqrt', min_samples_split=10, n_estimators=100)


DF_BANCADA = read_sql_query(analise_bancada_completa, DW.get_engine())
DF_LEITURA = read_sql_query(hidrometros_bancada_medicoes, DW.get_engine())
DF = pipeline_from_bancada_completa(DF_BANCADA, DF_LEITURA, DW)


MODELO, FITED_SCALER = predicao_treino(DF, RFC, SCALER)
joblib.dump(MODELO, './model/modelo_treinado.cagece')
joblib.dump(FITED_SCALER, './model/scaler_treinado.cagece')
