# NGSPICE
Automatizando a criação de arquivos spice para simulação de circuitos de transistores.  
  
**Objetivo**  
Conseguir implementar uma ferramenta capaz de obter os atrasos de propagação de uma função lógica e criar os
comandos de measure para o NGSPICE.  
  
**Metodologia e Procedimentos**  
  
Cada dupla deverá implementar, na linguagem de sua preferência um algoritmo para encontrar todos os
possíveis atrasos de propagação de uma função lógica. Além disso, será necessário que a ferramenta forneça as
PWLs para estimular os atrasos e os comandos de measure do NGSPICE.  
O algoritmo receberá como entrada somente a saída da tabela verdade em hexadecimal e o nome das entradas
do circuito. Deverá fornecer todos os atrasos de propagação, as ondas PWL de estímulo para os atrasos e os
comandos de measure.  
  
fontes - A B C | saida  
linha0 - 0 0 0 | 1  
linha1 - 0 0 1 | 1  
linha2 - 0 1 0 | 1  
linha3 - 0 1 1 | 0  
linha4 - 1 0 0 | 0  
linha5 - 1 0 1 | 0  
linha6 - 1 1 0 | 0  
linha7 - 1 1 1 | 0  
  
atrasos:  
linha0 para linha4 tphl fonteA  
linha4 para linha0 tplh fonteA  
  
linha1 para linha3 tphl fonteB  
linha3 para linha1 tplh fonteB  
  
linha1 para linha5 tphl fonteA  
linha5 para linha1 tplh fonteA  
  
linha2 para linha3 tphl fonteC  
linha3 para linha2 tplh fonteC  
  
linha2 para linha6 tphl fonteA  
linha6 para linha2 tplh fonteA  
  
