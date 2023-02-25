from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from pandas import read_csv

scaler = StandardScaler()
df = read_csv('./data/HidrometrosML_TRAIN.csv')
previsores = ['CVProcessado', 'vidaInstalacao',\
                  'vidaHidrometro','IMO_QTD_PONTOS_UTILIZACAO','QtdMedicoes',\
                  'QtdOcorrencias','QTD_INSTALACOES', 'variacaoTendencia']
classe = df['status'].values
previsor = scaler.fit_transform(df[previsores])

rfc = RandomForestClassifier()
params_rfc = { 
    'bootstrap': [True, False],
    'n_estimators': [100,200, 500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8,9,10,11,12,13,14],
    'criterion' :['gini', 'entropy'],
    'min_samples_split': [2,4,6,8,10]
}
CV_rfc = GridSearchCV(estimator=rfc, param_grid=params_rfc,cv= 10, n_jobs=3)
CV_rfc.fit(previsor, classe)
CV_rfc.best_params_
# {'bootstrap': True,
#  'criterion': 'gini',
#  'max_depth': 9,
#  'max_features': 'auto',
#  'min_samples_split': 2,
#  'n_estimators': 200}
