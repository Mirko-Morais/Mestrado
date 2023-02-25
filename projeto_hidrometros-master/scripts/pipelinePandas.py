import sys ; sys.path.append('./scripts')
from utils import pdmunging as pdm
from utils import eda_hidrometros as eda
from pandas import merge as merge
from pandas import read_csv, read_sql_query
from pandas import Timestamp
from numpy import nan, inf
import operator

def pipeline_from_cliente( path_serv70, pathEtlImoveis, pathEtlLeituras,pathOutputFile, periodoMeses, tipoPipeline):
      
      map_columns_servico_70 = {'bhc_dsc_un': 'UN',
      'bhc_dat_verificacao': 'dataVerificacao', 
      'bhc_cod_hidrometro':'IDHidrometro',
      'bhc_dat_instalacao': 'dataInstalacao',
      'bhc_vlr_qn':'Qn', 
      'bhc_vlr_qt':'Qt',
      'bhc_vlr_qmin':'Qmin',
      'bhc_dsc_status':'status',
      'bhc_dsc_tip_reprovacao':'tipoReprovacao', 
      'bhc_dsc_impedimento':'Impedimento'}
      df_servico_70 = path_serv70.rename(columns=map_columns_servico_70)
      # df_servico_70 = read_csv(path_serv70,decimal=',', thousands='.',\
      #                   names=['UN','dataVerificacao','IDHidrometro','dataInstalacao', 'Qn', \
      #                         'Qt', 'Qmin', 'status', 'tipoReprovacao', 'Impedimento'], skiprows=1,\
      #                         parse_dates=['dataVerificacao', 'dataInstalacao'])

      df_servico_70.pipe(eda.RemoveEspaco, col='IDHidrometro', value='')\
                  .pipe(eda.CalculaPerda,  cols=['Qt', 'Qmin', 'Qn'], factors=[0.7403, 0.1838, 0.0759], colName='Perda' )

      df_servico_70 = df_servico_70[df_servico_70['Impedimento'].isna()]

      # colunas_leitura = ['MED_NUM_SEQ_MEDIDOR','MED_NUM_MEDIDOR','MED_DAT_CADASTRO_MEDIDOR','MAR_SEQ_MARCA',\
      #       'ILM_SEQ_ITEM_LOTE_MEDIDOR','MED_STA_MEDIDOR','ESM_SEQ_ESPECIFICACAO_MEDIDOR',\
      #       'INS_DAT_INSTALACAO_MEDIDOR','INS_DAT_RETIRADA_MEDIDOR','MED_NUM_LEITURA_CAMPO_ANT',\
      #       'MED_NUM_LEITURA_PROC_ANT','MED_NUM_LEITURA_CAMPO_ATUAL','MED_NUM_LEITURA_PROC_ATUAL',\
      #       'MED_DAT_LEITURA','OCL_SEQ_OCORRENCIA_CAMPO','IMO_COD_INSCRICAO','PRO_SEQ_PRODUTO', 'QTD_INSTALACOES']
      # df_leitura = read_csv(pathEtlLeituras, names=colunas_leitura, low_memory=False, \
      #                   parse_dates=['MED_DAT_CADASTRO_MEDIDOR','INS_DAT_INSTALACAO_MEDIDOR',\
      #                               'INS_DAT_RETIRADA_MEDIDOR','MED_DAT_LEITURA'], \
      #                   decimal='.', thousands=',')
      colunas_leitura = ['hmh_num_medidor', 'hmh_num_seq_medidor', 'hmh_dat_cadastro_medidor',
       'hmh_cod_marca', 'hmh_cod_item_lote_medidor', 'hmh_cod_sta_medidor',
       'hmh_cod_especificacao_medidor', 'hmh_dat_instalacao_medidor',
       'hmh_dat_retirada_medidor', 'hmh_num_leitura_campo_ant',
       'hmh_num_leitura_proc_ant', 'hmh_num_leitura_campo_atual',
       'hmh_num_leitura_proc_atual', 'hmh_dat_leitura',
       'hmh_cod_ocorrencia_campo', 'hmh_cod_inscricao', 'hmh_cod_produto',
       'hmh_dat_qtd_instalacao', 'hmh_dsc_tip_registro']

      labels_leitura = ['MED_NUM_SEQ_MEDIDOR','MED_NUM_MEDIDOR','MED_DAT_CADASTRO_MEDIDOR','MAR_SEQ_MARCA',\
            'ILM_SEQ_ITEM_LOTE_MEDIDOR','MED_STA_MEDIDOR','ESM_SEQ_ESPECIFICACAO_MEDIDOR',\
            'INS_DAT_INSTALACAO_MEDIDOR','INS_DAT_RETIRADA_MEDIDOR','MED_NUM_LEITURA_CAMPO_ANT',\
            'MED_NUM_LEITURA_PROC_ANT','MED_NUM_LEITURA_CAMPO_ATUAL','MED_NUM_LEITURA_PROC_ATUAL',\
            'MED_DAT_LEITURA','OCL_SEQ_OCORRENCIA_CAMPO','IMO_COD_INSCRICAO','PRO_SEQ_PRODUTO', 'QTD_INSTALACOES', 'TIPO_REGISTRO']

      map_columns_leitura = dict(zip(colunas_leitura, labels_leitura))   

      df_leitura = pathEtlLeituras.rename(columns=map_columns_leitura)

      # colunas_imovel = ['IMO_COD_INSCRICAO','IMO_QTD_PONTOS_UTILIZACAO','PIM_SEQ_PADRAO_IMOVEL',\
      #                   'IMO_QTD_AREA_COBERTA','TIC_SEQ_TIP_CONSTRUCAO','UAD_COD_UNIDADE_ADMINISTRATIVA',\
      #                   'SET_TIP_SETOR']
      # df_imovel = read_csv(pathEtlImoveis,  names=colunas_imovel)
      colunas_imovel =  ['IMO_COD_INSCRICAO','IMO_QTD_PONTOS_UTILIZACAO','PIM_SEQ_PADRAO_IMOVEL',\
                        'IMO_QTD_AREA_COBERTA','TIC_SEQ_TIP_CONSTRUCAO','UAD_COD_UNIDADE_ADMINISTRATIVA',\
                        'SET_TIP_SETOR', 'TIPO_REGISTRO']
      labels_imovel = ['hid_imo_cod_inscricao', 'hid_imo_qtd_pontos_utilizacao',
       'hid_imo_seq_padrao_imovel', 'hid_imo_qtd_area_coberta',
       'hid_imo_seq_tip_construcao', 'hid_imo_cod_unidade_administrativa',
       'hid_imo_tip_setor', 'hid_imo_cod_tip_registro']

      map_columns_imovel = dict(zip(labels_imovel, colunas_imovel)) 
      df_imovel = pathEtlImoveis.rename(columns=map_columns_imovel)      

      df_leitura.pipe(eda.RelacionaColuna, colName='IDHidrometro', col1=df_leitura['MED_NUM_MEDIDOR'].astype(object), \
                  col2=df_leitura['MED_NUM_SEQ_MEDIDOR'].astype(str), operador=operator.concat)\
            .pipe(eda.AnoMedidorLacre, col='MED_NUM_MEDIDOR', colName='MED_ANO_MEDIDOR')\
            .pipe(eda.RelacionaColuna, colName='ConsumoProcessado', col1=df_leitura.MED_NUM_LEITURA_PROC_ATUAL, \
                  col2=df_leitura.MED_NUM_LEITURA_PROC_ANT, operador=operator.sub)\
            .pipe(eda.RelacionaColuna, colName='ConsumoMedido', col1=df_leitura.MED_NUM_LEITURA_CAMPO_ATUAL, \
                  col2=df_leitura.MED_NUM_LEITURA_CAMPO_ANT, operador=operator.sub)\
            .pipe(eda.TrataNegativos, col='ConsumoProcessado', use=nan)\
            .pipe(eda.ColunaTransformada,  colName='MedianaProcessado', groupby='IDHidrometro', \
                  col='ConsumoProcessado', operation='median')\
            .pipe(eda.ColunaTransformada,  colName='QtdMedicoes', groupby='MED_NUM_SEQ_MEDIDOR', \
                  col='IMO_COD_INSCRICAO', operation='count')\
            .pipe(eda.ColunaTransformada,  colName='MediaProcessado', groupby='IDHidrometro', \
                  col='ConsumoProcessado', operation='mean')\
            .pipe(eda.ColunaTransformada,  colName='DesvioPadraoProcessado', groupby='IDHidrometro', \
                  col='ConsumoProcessado', operation='std')\
            .pipe(eda.RelacionaColuna, colName='CVProcessado', col1=df_leitura.DesvioPadraoProcessado, \
                  col2=df_leitura.MediaProcessado, operador=operator.truediv)\
            .pipe(eda.AplicaFuncao, colName='isOcorrencia', col='OCL_SEQ_OCORRENCIA_CAMPO',\
                  funcao = lambda x: 1 if x > 0 else 0 )\
            .pipe(eda.ColunaTransformada,  colName='QtdOcorrencias', groupby='IDHidrometro', \
                  col='isOcorrencia', operation='sum')\
            .pipe(eda.ColunaTransformada,  colName='variacaoTendencia', groupby='IDHidrometro', \
                  col='ConsumoProcessado', operation=eda.trendserie)

      colunas_analise = ['IDHidrometro','MED_ANO_MEDIDOR', 'IMO_COD_INSCRICAO', 'MAR_SEQ_MARCA', \
                        'ESM_SEQ_ESPECIFICACAO_MEDIDOR','MedianaProcessado', 'MediaProcessado', \
                        'DesvioPadraoProcessado','CVProcessado', 'QtdOcorrencias', 'INS_DAT_INSTALACAO_MEDIDOR', 'QtdMedicoes', 'QTD_INSTALACOES', 'variacaoTendencia']
      df_leitura = df_leitura[colunas_analise].drop_duplicates(keep='first')

      df = pdmerge(df_servico_70, df_leitura, how='left', \
                  on="IDHidrometro", suffixes=('_srv70', '_medicao'))
      df = pdmerge(df, df_imovel, how='left', \
                  on="IMO_COD_INSCRICAO", suffixes=('_df', '_imovel'))

      df.pipe(eda.TrataNA, col='dataInstalacao', use=df['INS_DAT_INSTALACAO_MEDIDOR'])\
      .pipe(eda.Recorta, col='status' , start_position=0, end_position=2)\
      .pipe(eda.AplicaFuncao, colName='anoInstalacao', col='dataInstalacao',\
                  funcao = lambda x: Timestamp(x).year )\
      .pipe(eda.AplicaFuncao, colName='anoRetirada', col='dataVerificacao',\
                  funcao = lambda x: Timestamp(x).year )\
      .pipe(eda.RelacionaColuna, colName='vidaInstalacao', col1=df['anoRetirada'], \
                  col2=df['anoInstalacao'], operador=operator.sub)\
      .pipe(eda.RelacionaColuna, colName='vidaHidrometro', col1=df['anoRetirada'], \
                  col2=df['MED_ANO_MEDIDOR'], operador=operator.sub)\
      .pipe(eda.setOutlier, 'CVProcessado', 'outCV')\
      .pipe(eda.setOutlier, 'variacaoTendencia', 'outVarTend')

      remover_do_df = ['UN', 'dataVerificacao', 'IDHidrometro', 'dataInstalacao', 'Qn', 'Qt', 'Qmin', \
                  'tipoReprovacao', 'Impedimento', 'Perda', 'MED_ANO_MEDIDOR', 'IMO_COD_INSCRICAO', \
                  'INS_DAT_INSTALACAO_MEDIDOR','SET_TIP_SETOR', 'anoInstalacao', 'anoRetirada', \
                  'TIC_SEQ_TIP_CONSTRUCAO', 'IMO_QTD_AREA_COBERTA', 'DesvioPadraoProcessado', \
                  'MediaProcessado', 'MedianaProcessado' ]
      df.drop(columns=remover_do_df, inplace=True)

      aplicar_onehotencoding = ['MAR_SEQ_MARCA','ESM_SEQ_ESPECIFICACAO_MEDIDOR', \
            'PIM_SEQ_PADRAO_IMOVEL', 'UAD_COD_UNIDADE_ADMINISTRATIVA']
      for categoria in aplicar_onehotencoding:
        df = pdm.set_onehotencoding(df, categoria, categoria)

      df.dropna(inplace=True)
      
      status_map = {'RP': 0, 'AP': 1}
      df['status'] = df['status'].map(status_map)

      if tipoPipeline == 'train':
            df.drop(df[df.QtdMedicoes>periodoMeses].index, inplace=True)
            df.drop(df[df['outCV'] ==1].index, inplace=True)
            df.drop(df[df['outVarTend'] ==1].index, inplace=True)
            df.to_csv(pathOutputFile, index=False)
      elif tipoPipeline == 'test':
            df.drop(df[df.QtdMedicoes>periodoMeses].index, inplace=True)
            df.replace([inf, -inf], 1)
            df.pipe(eda.TrataNA, col='variacaoTendencia', use=df.variacaoTendencia.median())
            df.to_csv(pathOutputFile, index=False)

      return df

def pipeline_from_producao(df_leitura):
  df_leitura.pipe(eda.RelacionaColuna, colName='IDHidrometro', col1=df_leitura['MED_NUM_MEDIDOR'].astype(object), \
                    col2=df_leitura['MED_NUM_SEQ_MEDIDOR'].astype(str), operador=operator.concat)\
              .pipe(eda.AnoMedidorLacre, col='MED_NUM_MEDIDOR', colName='MED_ANO_MEDIDOR')\
              .pipe(eda.RelacionaColuna, colName='ConsumoProcessado', col1=df_leitura.MED_NUM_LEITURA_PROC_ATUAL, \
                    col2=df_leitura.MED_NUM_LEITURA_PROC_ANT, operador=operator.sub)\
              .pipe(eda.RelacionaColuna, colName='ConsumoMedido', col1=df_leitura.MED_NUM_LEITURA_CAMPO_ATUAL, \
                    col2=df_leitura.MED_NUM_LEITURA_CAMPO_ANT, operador=operator.sub)\
              .pipe(eda.TrataNegativos, col='ConsumoProcessado', use=nan)\
              .pipe(eda.ColunaTransformada,  colName='MedianaProcessado', groupby='IDHidrometro', \
                    col='ConsumoProcessado', operation='median')\
              .pipe(eda.ColunaTransformada,  colName='QtdMedicoes', groupby='MED_NUM_SEQ_MEDIDOR', \
                    col='IMO_COD_INSCRICAO', operation='count')\
              .pipe(eda.ColunaTransformada,  colName='MediaProcessado', groupby='IDHidrometro', \
                    col='ConsumoProcessado', operation='mean')\
              .pipe(eda.ColunaTransformada,  colName='DesvioPadraoProcessado', groupby='IDHidrometro', \
                    col='ConsumoProcessado', operation='std')\
              .pipe(eda.RelacionaColuna, colName='CVProcessado', col1=df_leitura.DesvioPadraoProcessado, \
                    col2=df_leitura.MediaProcessado, operador=operator.truediv)\
              .pipe(eda.AplicaFuncao, colName='isOcorrencia', col='OCL_SEQ_OCORRENCIA_CAMPO',\
                    funcao = lambda x: 1 if x > 0 else 0 )\
              .pipe(eda.ColunaTransformada,  colName='QtdOcorrencias', groupby='IDHidrometro', \
                    col='isOcorrencia', operation='sum')\
              .pipe(eda.ColunaTransformada,  colName='variacaoTendencia', groupby='IDHidrometro', \
                    col='ConsumoProcessado', operation=eda.trendserie)

  colunas_analise = ['IDHidrometro','MED_ANO_MEDIDOR', 'IMO_COD_INSCRICAO', 'MAR_SEQ_MARCA', \
                      'ESM_SEQ_ESPECIFICACAO_MEDIDOR','MedianaProcessado', 'MediaProcessado', \
                      'DesvioPadraoProcessado','CVProcessado', 'QtdOcorrencias', \
                      'INS_DAT_INSTALACAO_MEDIDOR', 'QtdMedicoes', 'qtd_instalacao', \
                      'variacaoTendencia', 'hid_imo_qtd_pontos_utilizacao']
  df_leitura = df_leitura[colunas_analise].drop_duplicates(keep='first')

  df_leitura['dataVerificacao'] = Timestamp.today()

  df_leitura.pipe(eda.AplicaFuncao, colName='anoInstalacao', col='INS_DAT_INSTALACAO_MEDIDOR',\
                    funcao = lambda x: Timestamp(x).year )\
        .pipe(eda.AplicaFuncao, colName='anoRetirada', col='dataVerificacao',\
                    funcao = lambda x: Timestamp(x).year )\
        .pipe(eda.RelacionaColuna, colName='vidaInstalacao', col1=df_leitura['anoRetirada'], \
                    col2=df_leitura['anoInstalacao'], operador=operator.sub)\
        .pipe(eda.RelacionaColuna, colName='vidaHidrometro', col1=df_leitura['anoRetirada'], \
                    col2=df_leitura['MED_ANO_MEDIDOR'], operador=operator.sub)\
        .pipe(eda.setOutlier, 'CVProcessado', 'outCV')\
        .pipe(eda.setOutlier, 'variacaoTendencia', 'outVarTend')

  cols = ['CVProcessado', 'vidaInstalacao',\
                    'vidaHidrometro','hid_imo_qtd_pontos_utilizacao','QtdMedicoes',\
                    'QtdOcorrencias','qtd_instalacao', 'variacaoTendencia', 'IDHidrometro']

  df_leitura.replace([inf, -inf], 1)
  df_leitura.pipe(eda.TrataNA, col='CVProcessado', use=df_leitura.CVProcessado.median())      

  return df_leitura[cols].copy()

def pipeline_from_bancada_completa(df_bancada, df_leitura, db_instance,periodo=25):
  df_bancada.pipe(eda.RemoveEspaco, col='bhc_cod_hidrometro', value='')\
      .pipe(eda.CalculaPerda,  cols=['bhc_vlr_qt', 'bhc_vlr_qmin', 'bhc_vlr_qn'], factors=[0.7403, 0.1838, 0.0759], colName='Perda')
  df_servico_70 = df_bancada[df_bancada['bhc_dsc_impedimento'].isna()]


  df_leitura.pipe(eda.RelacionaColuna, colName='IDHidrometro', \
        col1=df_leitura['med_num_medidor'].astype(object),\
        col2=df_leitura['med_num_seq_medidor'].astype(str), operador=operator.concat)\
      .pipe(eda.AnoMedidorLacre, col='med_num_medidor', colName='med_ano_medidor')\
      .pipe(eda.RelacionaColuna, colName='ConsumoProcessado', \
        col1=df_leitura.med_num_leitura_proc_atual,\
        col2=df_leitura.med_num_leitura_proc_ant, operador=operator.sub)\
      .pipe(eda.RelacionaColuna, colName='ConsumoMedido', \
        col1=df_leitura.med_num_leitura_campo_atual,
        col2=df_leitura.med_num_leitura_campo_ant, operador=operator.sub)\
      .pipe(eda.TrataNegativos, col='ConsumoProcessado', use=nan)\
      .pipe(eda.ColunaTransformada,  colName='MedianaProcessado', groupby='IDHidrometro',
            col='ConsumoProcessado', operation='median')\
      .pipe(eda.ColunaTransformada,  colName='QtdMedicoes', groupby='med_num_seq_medidor',
            col='hid_imo_cod_inscricao', operation='count')\
      .pipe(eda.ColunaTransformada,  colName='MediaProcessado', groupby='IDHidrometro',
            col='ConsumoProcessado', operation='mean')\
      .pipe(eda.ColunaTransformada,  colName='DesvioPadraoProcessado', groupby='IDHidrometro',
            col='ConsumoProcessado', operation='std')\
      .pipe(eda.RelacionaColuna, colName='CVProcessado', col1=df_leitura.DesvioPadraoProcessado,
            col2=df_leitura.MediaProcessado, operador=operator.truediv)\
      .pipe(eda.AplicaFuncao, colName='isOcorrencia', col='ocl_seq_ocorrencia_campo',
            funcao=lambda x: 1 if x > 0 else 0)\
      .pipe(eda.ColunaTransformada,  colName='QtdOcorrencias', groupby='IDHidrometro',
            col='isOcorrencia', operation='sum')\
      .pipe(eda.ColunaTransformada,  colName='variacaoTendencia', groupby='IDHidrometro',
            col='ConsumoProcessado', operation=eda.trendserie)

  colunas_analise = ['IDHidrometro','med_ano_medidor', 'hid_imo_cod_inscricao', 
                    'mar_seq_marca','esm_seq_especificacao_medidor','MedianaProcessado', 
                    'MediaProcessado','DesvioPadraoProcessado','CVProcessado', 
                    'QtdOcorrencias', 'ins_dat_instalacao_medidor', 'QtdMedicoes', 
                    'qtd_instalacao', 'variacaoTendencia', 'hid_imo_qtd_pontos_utilizacao']

  df_leitura = df_leitura[colunas_analise].drop_duplicates(keep='first')

  df = merge(df_servico_70, df_leitura, how='left', left_on='bhc_cod_hidrometro',\
    right_on='IDHidrometro', suffixes=('_srv70', '_medicao'))

  df.pipe(eda.TrataNA, col='bhc_dat_instalacao', use=df['ins_dat_instalacao_medidor'])\
  .pipe(eda.Recorta, col='bhc_dsc_status' , start_position=0, end_position=2)\
  .pipe(eda.AplicaFuncao, colName='anoInstalacao', col='bhc_dat_instalacao',\
              funcao = lambda x: Timestamp(x).year )\
  .pipe(eda.AplicaFuncao, colName='anoRetirada', col='bhc_dat_verificacao',\
              funcao = lambda x: Timestamp(x).year )\
  .pipe(eda.RelacionaColuna, colName='vidaInstalacao', col1=df['anoRetirada'], \
              col2=df['anoInstalacao'], operador=operator.sub)\
  .pipe(eda.RelacionaColuna, colName='vidaHidrometro', col1=df['anoRetirada'], \
              col2=df['med_ano_medidor'], operador=operator.sub)\
  .pipe(eda.setOutlier, 'CVProcessado', 'outCV')\
  .pipe(eda.setOutlier, 'variacaoTendencia', 'outVarTend')

  status_map = {'RP': 0, 'AP': 1}
  df['bhc_dsc_status'] = df['bhc_dsc_status'].map(status_map)

  df.drop(df[df.QtdMedicoes>periodo].index, inplace=True)
  df.drop(df[df['outCV'] ==1].index, inplace=True)
  df.drop(df[df['outVarTend'] ==1].index, inplace=True)
  df.replace([inf, -inf], 1)
  df.pipe(eda.TrataNA, col='CVProcessado', use=df.CVProcessado.median()) 

  cols = ['CVProcessado', 'vidaInstalacao','vidaHidrometro','hid_imo_qtd_pontos_utilizacao',
    'QtdMedicoes','QtdOcorrencias','qtd_instalacao', 'variacaoTendencia','bhc_dsc_status','IDHidrometro']
  df = df[cols]

  df.to_sql('hid_var_variaveis_modelo', db_instance.get_engine(), schema='ml',if_exists='replace')  
  return df
