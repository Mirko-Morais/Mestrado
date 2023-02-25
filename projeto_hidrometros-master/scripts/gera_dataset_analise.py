'''
Carrega Imoveis e predições e salva em JOBLIB
'''
from pandas import read_sql_query
from pandas import merge
from sklearn.externals import joblib
from etl.database import Prax, Vertica
from etl.sql_queries import IMOVEIS_ATIVOS_PRODUCAO
from etl.sql_queries import predicoes_realizadas


PRAX = Prax()
VERTICA = Vertica()
IMOVEIS_ATIVOS = read_sql_query(IMOVEIS_ATIVOS_PRODUCAO, PRAX.get_engine())
PREDICOES = read_sql_query(predicoes_realizadas, VERTICA.get_engine())
DF = merge(PREDICOES, IMOVEIS_ATIVOS, how='inner', \
  left_on='hid_imo_cod_inscricao', right_on='imo_bsk_imovel')


colunas = {'CVProcessado': 'float32',
 'ESM_SEQ_ESPECIFICACAO_MEDIDOR': 'int8',
 'IDHidrometro': 'category',
 'MED_NUM_VOLUME_CALCULADO': 'float32',
 'MED_NUM_VOLUME_MEDIDO': 'float32',
 'QtdMedicoes': 'int8',
 'QtdOcorrencias': 'int8',
 'geo_lge_dsc_distrito_prax': 'category',
 'geo_lge_dsc_localidade_prax': 'category',
 'geo_lge_dsc_municipio_prax': 'category',
 'geo_set_num_setor': 'int16',
 'geo_uad_sgl_unidade_negocio': 'category',
 'hid_imo_cod_inscricao': 'int64',
 'hid_imo_qtd_pontos_utilizacao':'int8',
 'imo_bsk_imovel': 'int64',
 'pim_dsc_padrao_imovel': 'category',
 'predicao': 'int8',
 'proba_0': 'float16',
 'sii_nom_situacao_imovel':'category',
 'sla_nom_situacao_lig_agua': 'int8',
 'variacaoTendencia': 'float32',
 'vidaHidrometro': 'int8',
 'vidaInstalacao': 'int8'}

DF = DF.astype(colunas) 
joblib.dump(DF, './data/df_analise.cagece')
