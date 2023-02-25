from pandas import read_csv
from pandas import DateOffset

def gravaPeriodoPorHidrometro(pathInput, pathOutput, intevaloMeses):
    df = read_csv(pathInput,decimal=',', thousands='.', 
                       names=['UN','dataVerificacao','IDHidrometro','dataInstalacao', 
                       'Qn', 'Qt', 'Qmin', 'status', 'tipoReprovacao', 'Impedimento'], 
                       skiprows=1, parse_dates=['dataVerificacao', 'dataInstalacao'])
    df['dataVerificacaoINI'] = df['dataVerificacao'] - DateOffset(months=intevaloMeses)
    df[['dataVerificacao', 'dataVerificacaoINI', 'IDHidrometro']]\
        .drop_duplicates(keep='first').to_csv(pathOutput, index=False, date_format='%Y%m')

gravaPeriodoPorHidrometro('./data/serv70_2018.csv', './data/PeriodoPorHidrometro_TRAIN.csv', 25)
gravaPeriodoPorHidrometro('./data/serv70_2019.csv', './data/PeriodoPorHidrometro_TEST.csv', 25)
