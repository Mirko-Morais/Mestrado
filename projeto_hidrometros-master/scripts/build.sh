
# Fluxo de build do modelo 

# APAGAR TODAS AS PLANILHAS GERADAS NO PROCESSO
# POIS O PROCESSO DE ETL ADICIONA GRADATIVAMENTE OS 
# REGISTROS NOS ARQUIVOS CSV
# Carrega ultimo lote dos hidrometros 
sh $KETTLE/pan.sh ETL_PROCESSA_ULTIMO_LOTE.ktr

# Carrega leituras com base no raio definido de tempo em meses
python3 gravaPeriodoPorHidrometro.py

# processar etl para carregar as leituras de cada hidrometro no prax.
sh $KETTLE/pan.sh ETL_PROCESSA_COLETAS.ktr

# gravar Imoveis dentro do periodo
python3 gravaImoveisNoPeriodo.py

# coletar dados de imoveis dessas leituras.
sh $KETTLE/pan.sh ETL_PROCESSA_IMOVEIS.ktr

# pipeline pandas
python3 pipelinePandas.py

# pipeline sklearn
python3 pipelineSkLearn.py
