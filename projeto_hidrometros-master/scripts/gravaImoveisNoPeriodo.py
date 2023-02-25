from pandas import  read_csv

def gravaImoveisNoPeriodo(pathInput, pathOutput):
    colunas_leitura = ['MED_NUM_SEQ_MEDIDOR','MED_NUM_MEDIDOR','MED_DAT_CADASTRO_MEDIDOR','MAR_SEQ_MARCA',\
                                  'ILM_SEQ_ITEM_LOTE_MEDIDOR','MED_STA_MEDIDOR','ESM_SEQ_ESPECIFICACAO_MEDIDOR',\
                                  'INS_DAT_INSTALACAO_MEDIDOR','INS_DAT_RETIRADA_MEDIDOR','MED_NUM_LEITURA_CAMPO_ANT',\
                                  'MED_NUM_LEITURA_PROC_ANT','MED_NUM_LEITURA_CAMPO_ATUAL','MED_NUM_LEITURA_PROC_ATUAL',\
                                  'MED_DAT_LEITURA','OCL_SEQ_OCORRENCIA_CAMPO','IMO_COD_INSCRICAO','PRO_SEQ_PRODUTO', 'QTD_INSTALACOES']
    df_leitura = read_csv(pathInput, names=colunas_leitura, 
                                        low_memory=False,  parse_dates=['MED_DAT_CADASTRO_MEDIDOR',\
                                          'INS_DAT_INSTALACAO_MEDIDOR', 'INS_DAT_RETIRADA_MEDIDOR',
                                          'MED_DAT_LEITURA'],  decimal='.', thousands=',')
    df_leitura['IMO_COD_INSCRICAO'].drop_duplicates(keep='first').to_csv(pathOutput, index=False)  

gravaImoveisNoPeriodo( './data/DATASET_ETL_MEDICOES_TRAIN.csv', './data/ImoveisNoPeriodo_TRAIN.csv')
gravaImoveisNoPeriodo( './data/DATASET_ETL_MEDICOES_TEST.csv', './data/ImoveisNoPeriodo_TEST.csv')