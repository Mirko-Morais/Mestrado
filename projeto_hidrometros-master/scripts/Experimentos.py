# -*- coding: utf-8 -*-
import warnings ; warnings.filterwarnings("ignore", category=RuntimeWarning) 
import sys ; sys.path.append('scripts')
import Qualidade as qld
import pandas as pd
from numpy import unique
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC  
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier


df = pd.read_csv('./data/HidrometrosML_TRAIN.csv')

#target = 'status'
#features = [col for col in df.columns if col != target]

previsor = df.drop(columns='status').values
previsores2 = df[['CVProcessado', 'vidaInstalacao',\
                  'vidaHidrometro','IMO_QTD_PONTOS_UTILIZACAO','QtdMedicoes',\
                  'QtdOcorrencias','QTD_INSTALACOES', 'variacaoTendencia']]

classe = df['status'].values

scaler = StandardScaler()
minMax = MinMaxScaler()
previsor = scaler.fit_transform(previsores2)

X_train, X_test, y_train, y_test = train_test_split(previsor,classe,\
                                                    random_state = 0)



randomForest = RandomForestClassifier(n_estimators = 90, \
                                      criterion = 'entropy', \
                                      random_state = 0)

qld.analise_modelo(model_instance = randomForest,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
precision    recall  f1-score   support

           0       0.40      0.40      0.40         5
           1       0.98      0.98      0.98       189

   micro avg       0.97      0.97      0.97       194
   macro avg       0.69      0.69      0.69       194
weighted avg       0.97      0.97      0.97       194

[{'Acuracy Score': 0.9690721649484536}, 
{'RMSE': 0.17586311452816475}, 
{'R2': -0.23174603174603137},
 {'MAE': 0.030927835051546393}, 
 {'Confusion Matrix': array([[  2,   3],
       [  3, 186]])}, 
{'F1 Score': 0.9841269841269841}, 
{'AUC ROC': 0.692063492063492}]

'''


feat = df.drop(columns='status').keys()
feat_labels = feat.get_values()
importancias = pd.DataFrame(randomForest.feature_importances_,\
                            feat_labels, columns=['importance'])
# cv 23% , vidaInstalacao 19,5%, vidaHidrometro 18,8% 
# qtdPontosInstalacao 13%, qtdOcorrencias 6%

decisionTree = DecisionTreeClassifier()
qld.analise_modelo(model_instance = decisionTree,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
 precision    recall  f1-score   support

           0       0.43      0.60      0.50         5
           1       0.99      0.98      0.98       189

   micro avg       0.97      0.97      0.97       194
   macro avg       0.71      0.79      0.74       194
weighted avg       0.97      0.97      0.97       194

[{'Acuracy Score': 0.9690721649484536}, 
{'RMSE': 0.17586311452816475}, 
{'R2': -0.23174603174603137}, 
{'MAE': 0.030927835051546393}, 
{'Confusion Matrix': array([[  3,   2],
       [  4, 185]])}, 
       {'F1 Score': 0.9840425531914894}, 
       {'AUC ROC': 0.7894179894179895}]
'''

svclassifier = SVC(kernel='rbf', gamma='scale')
qld.analise_modelo(model_instance = svclassifier,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
 precision    recall  f1-score   support

           0       0.50      0.40      0.44         5
           1       0.98      0.99      0.99       189

   micro avg       0.97      0.97      0.97       194
   macro avg       0.74      0.69      0.72       194
weighted avg       0.97      0.97      0.97       194

[{'Acuracy Score': 0.9742268041237113}, 
{'RMSE': 0.16054032476698388},
 {'R2': -0.026455026455026065}, 
 {'MAE': 0.02577319587628866},
  {'Confusion Matrix': array([[  2,   3],
       [  2, 187]])}, 
       {'F1 Score': 0.9868073878627968}, 
       {'AUC ROC': 0.6947089947089947}]

'''

lr = LogisticRegression()
qld.analise_modelo(model_instance = lr,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
precision    recall  f1-score   support

           0       0.33      0.60      0.43         5
           1       0.99      0.97      0.98       189

   micro avg       0.96      0.96      0.96       194
   macro avg       0.66      0.78      0.70       194
weighted avg       0.97      0.96      0.96       194

[{'Acuracy Score': 0.9587628865979382}, 
{'RMSE': 0.2030692330267238}, 
{'R2': -0.642328042328042}, 
{'MAE': 0.041237113402061855}, 
{'Confusion Matrix': array([[  3,   2],
       [  6, 183]])}, 
       {'F1 Score': 0.9786096256684492},
        {'AUC ROC': 0.7841269841269841}]

'''

knn = KNeighborsClassifier(n_neighbors=10, algorithm='kd_tree',\
                           p=1)
qld.analise_modelo(model_instance = knn,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
 precision    recall  f1-score   support

           0       0.00      0.00      0.00         5
           1       0.97      1.00      0.99       189

   micro avg       0.97      0.97      0.97       194
   macro avg       0.49      0.50      0.49       194
weighted avg       0.95      0.97      0.96       194

[{'Acuracy Score': 0.9742268041237113}, 
{'RMSE': 0.16054032476698388},
 {'R2': -0.026455026455026065}, 
 {'MAE': 0.02577319587628866}, 
 {'Confusion Matrix': array([[  0,   5],
       [  0, 189]])}, 
       {'F1 Score': 0.9869451697127937}, 
       {'AUC ROC': 0.5}]

'''
gb = GradientBoostingClassifier()
gb_model = qld.analise_modelo(model_instance = gb,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
              precision    recall  f1-score   support

           0       0.72      0.74      0.73       390
           1       0.83      0.82      0.82       608

   micro avg       0.79      0.79      0.79       998
   macro avg       0.78      0.78      0.78       998
weighted avg       0.79      0.79      0.79       998

[{'Acuracy Score': 0.7865731462925851},
 {'RMSE': 0.46198144303360805},
 {'R2': 0.10351720647773288},
 {'MAE': 0.21342685370741482},
 {'Confusion Matrix': array([[289, 101],
         [112, 496]])},
 {'F1 Score': 0.8232365145228216},
 {'AUC ROC': 0.7784075573549258}]
'''
gnb = GaussianNB()
qld.analise_modelo(model_instance = gnb,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
              precision    recall  f1-score   support

           0       0.66      0.68      0.67       390
           1       0.79      0.78      0.78       608

   micro avg       0.74      0.74      0.74       998
   macro avg       0.73      0.73      0.73       998
weighted avg       0.74      0.74      0.74       998

[{'Acuracy Score': 0.7384769539078156},
 {'RMSE': 0.5113932401705994},
 {'R2': -0.09850708502024275},
 {'MAE': 0.26152304609218435},
 {'Confusion Matrix': array([[265, 125],
         [136, 472]])},
 {'F1 Score': 0.7834024896265561},
 {'AUC ROC': 0.7279014844804319}]
'''

xgbc = XGBClassifier()
qld.analise_modelo(model_instance = xgbc,\
                x_train = X_train, \
                y_train = y_train, \
                x_test = X_test, \
                y_test = y_test)
'''
              precision    recall  f1-score   support

           0       0.71      0.74      0.72       390
           1       0.83      0.81      0.82       608

   micro avg       0.78      0.78      0.78       998
   macro avg       0.77      0.77      0.77       998
weighted avg       0.78      0.78      0.78       998

[{'Acuracy Score': 0.7805611222444889},
 {'RMSE': 0.4684430357636999},
 {'R2': 0.07826417004048591},
 {'MAE': 0.21943887775551102},
 {'Confusion Matrix': array([[287, 103],
         [116, 492]])},
 {'F1 Score': 0.8179551122194513},
 {'AUC ROC': 0.7725539811066127}]
'''