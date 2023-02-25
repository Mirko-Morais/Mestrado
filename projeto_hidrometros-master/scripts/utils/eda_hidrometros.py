from statsmodels.tsa.seasonal import seasonal_decompose
from numpy import isnan

def TipoHidrometroMap(df, col):
  LOM_COD_TIPO_LOTE_MAP = {1: 'NOVO', 2:'RECUPERADO'}
  df[col] = df[col].map(LOM_COD_TIPO_LOTE_MAP) 
  return df

def ConcatenaColuna(df, colName, col1, col2):
  df[colName] = df[col1]+df[col2]
  return df

def FiltraDataFrame(df, col , setfilter):  
    return df.loc[df[col].isin(setfilter)]

def AnoMedidorLacre(df, col, colName):
    montalista = lambda x: [str(n) for n  in x if n.isdigit()]
    nro = lambda x: int(''.join(x)) if len(x) > 0 else 0
    df[colName] = df[col].apply(lambda x: nro(montalista(x[1:3]))+2000 \
                                          if nro(montalista(x[1:3]))<19 else nro(montalista(x[1:3]))+1900)
    return df

def RelacionaColuna(df, colName, col1, col2, operador):
  df[colName] = operador(col1,col2)
  return df

def ColunaTransformada(df, colName, groupby, col, operation):
    df[colName] = df.groupby(groupby)[col].transform(operation)
    return df

def TrataNegativos(df, col, use):
    df.loc[df[col]<0, col] = use
    return df

def TrataNA(df, col, use):
    df[col] = df[col].fillna(use)
    return df

def RemoveLinha(df, col, value):
    df.drop(df[df[col] == value].index, inplace=True)
    return df

def RemoveEspaco(df, col, value):
    df[col] = df[col].replace(regex=r' ', value=value)
    return df

def CalculaPerda(df, cols, factors, colName):
    df[colName] = df.apply(lambda x: (x[cols[0]]*factors[0])\
                                      +(x[cols[1]]*factors[1])\
                                      +(x[cols[2]]*factors[2]) , axis=1)
    return df

def SpentNivelChanged(lst_faixas, prc_erro, spent_median):
    next_spent_limit = list(filter(lambda x: x>spent_median, lst_faixas))[0]
    spent_with_error = spent_median * (1+prc_erro)
    if (spent_with_error < next_spent_limit):
        return 0
    return 1 

def MudaraFaixa(df, colName):
    list_faixas = [0, 11, 16, 21, 51, 999999999]
    df[colName] = df.apply(lambda x: SpentNivelChanged(lst_faixas=list_faixas,\
                                                prc_erro = x['Perda'],\
                                                spent_median=x['MedianaProcessado']),\
                    axis=1)
    return df

def Recorta(df, col, start_position, end_position):
    df[col] = df[col].apply(lambda x: x[start_position:end_position])
    return df

def OcorrenciaPeriodo(df, colName, col):
    df[colName] = df[col].apply(lambda x: 1 if x > 0 else 0 )
    return df

def AplicaFuncao(df, colName, col, funcao):
    df[colName] = df[col].apply(funcao)
    return df


def onInterval(vMin, vMax, value):
    if value >= vMin and value <= vMax:
        return 0
    return 1
def setOutlier(df, colName, col):
    iqr = df[colName].quantile(.75) - df[colName].quantile(.25)
    inf_limit = df[colName].quantile(.25) - (iqr*1.5)
    sup_limit = df[colName].quantile(.75)+ (iqr*1.5)
    df[col] = df[colName].apply(lambda x: onInterval(inf_limit, sup_limit, x))
    return df

def trendserie(pdserie,freq=4):
    serie = pdserie.fillna(0)
    if len(serie) > freq:
        t = seasonal_decompose(serie.values,freq=freq).trend
        notna = t[~isnan(t)]
        return (notna[-1]/notna[0])-1 if notna[0] else 0
    return 0