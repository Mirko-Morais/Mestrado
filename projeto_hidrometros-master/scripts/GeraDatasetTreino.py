# -*- coding: utf-8 -*-
"""
1. Carrega os hidrometros
2. Separa amostragem(para coleta via etl)
3. Carrega medicoes
4. Exporta imoveis das medicoes para coleta de dados
5. Carrega imoveis coletados via etl
6. Aplica pipeline de tratamento para medicoes
7. Une Dataframes
8. Aplica pipeline ao dataframe

"""

import warnings ; warnings.filterwarnings("ignore", category=RuntimeWarning) 
import sys ; sys.path.append('./scripts')
import pdmunging as pdm
import eda_hidrometros as eda

from pandas import merge 
from pandas import Timestamp
from pandas.io.parsers import read_csv
import operator
import numpy as np


hidrometros = read_csv('./data/hidrometros_para_teste.csv',\
                       skiprows=1,\
                       names=['IDHidrometro'])
hidrometros['dataVerificacao'] = 201903
hidrometros['dataVerificacaoINI'] = 201801

Amostragem = hidrometros.sample(10000)
Amostragem.to_csv('../data/hidrometros_teste.csv', index=False)

colunas_medicoes = ['MED_NUM_SEQ_MEDIDOR',\
                   'MED_NUM_MEDIDOR','MED_DAT_CADASTRO_MEDIDOR',\
                   'MAR_SEQ_MARCA', 'ILM_SEQ_ITEM_LOTE_MEDIDOR',\
                   'MED_STA_MEDIDOR','ESM_SEQ_ESPECIFICACAO_MEDIDOR',\
                   'INS_DAT_INSTALACAO_MEDIDOR','INS_DAT_RETIRADA_MEDIDOR',\
                   'MED_NUM_LEITURA_CAMPO_ANT', 'MED_NUM_LEITURA_PROC_ANT',\
                   'MED_NUM_LEITURA_CAMPO_ATUAL','MED_NUM_LEITURA_PROC_ATUAL',\
                   'MED_DAT_LEITURA','OCL_SEQ_OCORRENCIA_CAMPO',\
                   'IMO_COD_INSCRICAO','PRO_SEQ_PRODUTO', 'QTD_INSTALACOES']
medicoes = read_csv('./data/DATASET_ETL_MEDICOES_TESTE.csv', \
                    names=colunas_medicoes,\
                    low_memory=False,\
                    parse_dates=['MED_DAT_CADASTRO_MEDIDOR',\
                                 'INS_DAT_INSTALACAO_MEDIDOR',                                
                                 'INS_DAT_RETIRADA_MEDIDOR','MED_DAT_LEITURA'],        
                                 decimal='.', thousands=',')

medicoes['IMO_COD_INSCRICAO'].drop_duplicates(keep='first')\
.to_csv('./data/imoveis_teste.csv', index=False)

colunas_imovel = ['IMO_COD_INSCRICAO','IMO_QTD_PONTOS_UTILIZACAO',\
                  'PIM_SEQ_PADRAO_IMOVEL','IMO_QTD_AREA_COBERTA',\
                  'TIC_SEQ_TIP_CONSTRUCAO','UAD_COD_UNIDADE_ADMINISTRATIVA',
                  'SET_TIP_SETOR']
imoveis = read_csv('./data/DATASET_ETL_IMOVEIS_TESTE.csv', names=colunas_imovel)

medicoes.pipe(eda.RelacionaColuna, colName='IDHidrometro', \
                    col1=medicoes['MED_NUM_MEDIDOR'].astype(object),\
                    col2=medicoes['MED_NUM_SEQ_MEDIDOR'].astype(str),\
                    operador=operator.concat)\
         .pipe(eda.AnoMedidorLacre, col='MED_NUM_MEDIDOR',\
                   colName='MED_ANO_MEDIDOR')\
         .pipe(eda.RelacionaColuna, colName='ConsumoProcessado',\
               col1=medicoes.MED_NUM_LEITURA_PROC_ATUAL,\
               col2=medicoes.MED_NUM_LEITURA_PROC_ANT,\
               operador=operator.sub)\
         .pipe(eda.RelacionaColuna, colName='ConsumoMedido',\
               col1=medicoes.MED_NUM_LEITURA_CAMPO_ATUAL,\
               col2=medicoes.MED_NUM_LEITURA_CAMPO_ANT, \
               operador=operator.sub)\
         .pipe(eda.TrataNegativos, col='ConsumoProcessado', use=np.nan)\
         .pipe(eda.ColunaTransformada,  colName='MedianaProcessado', \
               groupby='IDHidrometro',\
               col='ConsumoProcessado', \
               operation='median')\
         .pipe(eda.ColunaTransformada,\
               colName='QtdMedicoes',\
               groupby='MED_NUM_SEQ_MEDIDOR',\
               col='IMO_COD_INSCRICAO', \
               operation='count')\
         .pipe(eda.ColunaTransformada,\
               colName='MediaProcessado',\
               groupby='IDHidrometro',\
               col='ConsumoProcessado',\
               operation='mean')\
         .pipe(eda.ColunaTransformada,\
               colName='DesvioPadraoProcessado', \
               groupby='IDHidrometro',\
               col='ConsumoProcessado', \
               operation='std')\
         .pipe(eda.RelacionaColuna,\
               colName='CVProcessado',\
               col1=medicoes.DesvioPadraoProcessado,\
               col2=medicoes.MediaProcessado,\
               operador=operator.truediv)\
        .pipe(eda.AplicaFuncao, colName='isOcorrencia', \
              col='OCL_SEQ_OCORRENCIA_CAMPO',\
              funcao = lambda x: 1 if x > 0 else 0 )\
        .pipe(eda.ColunaTransformada,\
              colName='QtdOcorrencias',\
              groupby='IDHidrometro',\
               col='isOcorrencia', operation='sum')

colunas_analise = ['IDHidrometro','MED_ANO_MEDIDOR', \
                   'IMO_COD_INSCRICAO', 'MAR_SEQ_MARCA',\
                    'ESM_SEQ_ESPECIFICACAO_MEDIDOR','MedianaProcessado',\
                    'MediaProcessado', 'DesvioPadraoProcessado',\
                    'CVProcessado', 'QtdOcorrencias', \
                    'INS_DAT_INSTALACAO_MEDIDOR', 'QtdMedicoes', \
                    'QTD_INSTALACOES']
medicoes = medicoes[colunas_analise].drop_duplicates(keep='first')

df = merge(medicoes, imoveis, how='left',\
              on="IMO_COD_INSCRICAO", suffixes=('_df', '_imovel'))
df['dataInstalacao'] = np.nan
df['dataVerificacao'] = Timestamp('2019-04-01 00:00:00')
df['status'] = 'RP'

df.pipe(eda.TrataNA, col='dataInstalacao', use=df['INS_DAT_INSTALACAO_MEDIDOR'])\
  .pipe(eda.Recorta, col='status' , start_position=0, end_position=2)\
  .pipe(eda.AplicaFuncao, colName='anoInstalacao', col='dataInstalacao',\
              funcao = lambda x: Timestamp(x).year )\
  .pipe(eda.AplicaFuncao, colName='anoRetirada', col='dataVerificacao',\
              funcao = lambda x: Timestamp(x).year )\
  .pipe(eda.RelacionaColuna, colName='vidaInstalacao', col1=df['anoRetirada'],\
               col2=df['anoInstalacao'], operador=operator.sub)\
  .pipe(eda.RelacionaColuna, colName='vidaHidrometro', col1=df['anoRetirada'],\
               col2=df['MED_ANO_MEDIDOR'], operador=operator.sub)

df = df[['IDHidrometro','CVProcessado', 'vidaInstalacao',\
                  'vidaHidrometro','IMO_QTD_PONTOS_UTILIZACAO','QtdMedicoes',\
                  'QtdOcorrencias','QTD_INSTALACOES']]
df.dropna(inplace=True)

df.to_csv('./data/test_hidrometros.csv', index=False)

df.describe()



