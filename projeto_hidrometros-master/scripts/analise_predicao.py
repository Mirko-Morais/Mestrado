'''
Análise das predições realizadas
'''
from sklearn.externals import joblib
from pandas import read_csv

def gera_inscricoes(data_frame, min_proba, und_negocio, setor, min_vol=7):
    '''
    Retorna dataframe filtrado
    '''
    data_frame['provavel_mudanca'] = data_frame.apply(spent_nivel_change, axis=1)
    return data_frame[(data_frame.proba_0 > min_proba)&\
    (data_frame.sla_nom_situacao_lig_agua == 1)&\
    (data_frame.geo_uad_sgl_unidade_negocio == und_negocio)&\
    (data_frame.MED_NUM_VOLUME_CALCULADO > min_vol)&\
    (data_frame.geo_set_num_setor == setor)&\
    (data_frame.provavel_mudanca == 1)&\
    (data_frame.vidaInstalacao > 3)&\
    (data_frame.QtdMedicoes<=26)&\
    (data_frame.sii_nom_situacao_imovel=='EM USO')
    ]

def calcula_tamanho_amostra(desvio_padrao, erro_aceitavel, confianca, tamanho_populacao):
    """
    dado determinado desvio padrao e erro aceitavel determina
    o valor amostral necessário para explicar o fenomeno.
    https://edisciplinas.usp.br/pluginfile.php/1940343/mod_resource/content/2/amostragem_MauroGrisi21092016.pdf
    """
    parametros = {
        90: {
            'a':0.10,
            'z': 1.645
        },
        95: {
            'a':0.05,
            'z': 1.96
        },
        99: {
            'a':0.01,
            'z': 2.575
        }
    }
    squared = lambda x: x*x
    n_zero = squared(parametros[confianca]['z'])*(squared(desvio_padrao)/squared(erro_aceitavel))
    n_ajustado = (tamanho_populacao*round(n_zero))/(tamanho_populacao+round(n_zero))

    return round(n_ajustado)

def spent_nivel_change(data_frame, col_name='MED_NUM_VOLUME_CALCULADO', erro=0.25):
    """
    Dado a mediana calcula se mudará de faixa
    """
    median = data_frame[col_name]
    list_faixas = [0, 11, 16, 21, 51, 999999999]
    next_spent_limit = list(filter(lambda x: x > median, list_faixas))[0]
    spent_with_error = median * (1+erro)
    if spent_with_error < next_spent_limit:
        return 0
    return 1

DF = joblib.load('./data/df_analise.cagece')

MTS55 = gera_inscricoes(DF, 0.51, 'UN-MTS', 84)

MTS55.to_csv('./data/export_mts84.csv', index=False)


#MTS63.to_parquet('./data/export_mtn54.parquet.gzip',
#                compression='gzip', index=False)
                    
#DF.to_parquet('./data/df.parquet.gzip',
#            compression='gzip', index=False)

# MTN_63 = read_csv('./data/export_mts63.csv')
# MTN_63 = MTN_63[MTN_63.SELECIONADO == 1]

# http://cienciasecognicao.org/portal/wp-content/uploads/2011/09/Tamanho-da-Amostra-1-1.pdf
# desvio padrao da idade dos hidrometros
# erro aceitavel um quinto do desvio
AMOSTRA = MTS63.vidaHidrometro.describe()
calcula_tamanho_amostra(AMOSTRA['std'], AMOSTRA['std']*0.2, 99,\
  AMOSTRA['count'])
# 77 amostras para descrever com 95% de precisão 