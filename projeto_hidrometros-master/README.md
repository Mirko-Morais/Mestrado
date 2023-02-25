# > EDA - PROJETO HIDROMETROS

### Solução proposta  
> Modelo que defina o momento ideal de troca do hidrometro levando em consideração a perda de eficiência e a possível mudança de faixa._

### Variáveis que influenciam a vida útil
1. Pressão da rede
2. Volume medido durante a vida
3. Marca
4. Capacidade 
5. Qualidade da agua da rede
6. Recondicionamento

### Datasets
1. Hidrometros (PRAX).
2. Analises de conformidade (PEA) (Xls)

#### Observações 
-  Normativa do inmetro recomenda aferições/regulagens no periodo de 5 anos.
-  Hidrometros com mais de 10 anos de idade são descartados automáticamente.
-  Análise de perda aplicando perfil de consumo baseado na ABNT NBR 15538 e erros de medição verificados através do serviço 070.

>Um medidor (med_medidor) esta associado a uma ou mais ligacoes (lig_ligacao)  das quais possuem uma ou mais instalações (ins_instalacao) que por sua vez possuem uma ou mais medicoes(med_medicao)
