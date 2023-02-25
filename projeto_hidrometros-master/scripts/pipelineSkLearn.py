from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from utils.Qualidade import KFoldEstratificado
from pandas import read_csv


def predicao_producao(dataframe, modelo_treinado, scaler):
  data = dataframe.drop(columns=['IDHidrometro'])
  previsores = dataframe[['CVProcessado', 'vidaInstalacao',\
                  'vidaHidrometro','hid_imo_qtd_pontos_utilizacao','QtdMedicoes',\
                  'QtdOcorrencias','qtd_instalacao', 'variacaoTendencia']]
  previsores = scaler.transform(data)
  previsao_classe = modelo_treinado.predict(previsores)
  previsao_probabilidade = modelo_treinado.predict_proba(previsores)

  return dataframe, previsao_classe, previsao_probabilidade

def predicao_treino(dataframe, modelo , scaler):
  classe = dataframe['bhc_dsc_status'].values
  previsores = dataframe[['CVProcessado', 'vidaInstalacao',\
                  'vidaHidrometro','hid_imo_qtd_pontos_utilizacao','QtdMedicoes',\
                  'QtdOcorrencias','qtd_instalacao', 'variacaoTendencia']]           
  fited_scaler = scaler.fit(previsores) 
  previsores = fited_scaler.transform(previsores)
  modelo.fit(previsores, classe)
  k_fold = KFoldEstratificado(modelo, previsores, classe, 10, accuracy_score)
  print(k_fold)
  return modelo, fited_scaler