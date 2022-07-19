import math
lista_de_linhas_arquivo_final = []

def entrada_de_dados():
    global lista_de_linhas_arquivo_final
    nome_circuito = input("Digite o nome do circuito: ")
    valor_hexa = str(input("Digite o valor em hexadecimal: "))

    return nome_circuito, valor_exa


def gera_binario(dado_de_entrada):
    global lista_de_linhas_arquivo_final
    binario = bin(int(dado_de_entrada, 16))
    saida_tabela_verdade = f'{binario[2:]}'
    
    return saida_tabela_verdade


def cria_arquivo_spice(nome_circuito):
    arquivo = open(f'{nome_circuito}.txt', 'w+')

    # dados iniciais
    lista_de_linhas_arquivo_final.append(nome_circuito)
    lista_de_linhas_arquivo_final.append('\n*PARAMETROS')
    lista_de_linhas_arquivo_final.append('.include 32nm_HP.pm')
    lista_de_linhas_arquivo_final.append('\n*DECLARANDO FONTES DE TENSAO')
    lista_de_linhas_arquivo_final.append('Vvdd vdd gnd 1')
    lista_de_linhas_arquivo_final.append('\n*DECLARACAO DAS FONTES')

    return arquivo


# Escreve uma única vez no arquivo (chamar apenas no final)
def escreve_no_arquivo_spice(arquivo, dados_para_o_arquivo):
    for item in dados_para_o_arquivo:
        arquivo.write(item)
        arquivo.write('\n')
    
    arquivo.close()


def define_numero_de_fontes(tamanho_saida):
    numero_de_fontes = math.log(tamanho_saida, 2)

    return int(numero_de_fontes)


def gera_tabela_verdade(numero_de_fontes, saida_tabela):
    quantidade_de_zeros = len(saida_tabela)
    tabela = []
    coluna = []
    for _ in range(numero_de_fontes):
        quantidade_de_zeros //= 2
        
        while len(coluna) < len(saida_tabela):
            for _ in range(quantidade_de_zeros):
                coluna.append(0)

            for _ in range(quantidade_de_zeros):
                coluna.append(1)
        
        tabela.append(coluna)
        coluna = []
   
    for caracter in saida_tabela:
        coluna.append(int(caracter))

    tabela.append(coluna)

    return tabela


def pwl(tabela_verdade):
    pwls = []
    for elemento in range(len(tabela_verdade) - 1):
        intervalo = f'Vfonte{elemento} fonte{elemento} gnd PWL (0ns 0 '

        for sinal in range(len(tabela_verdade[elemento]) - 1):

            if tabela_verdade[elemento][sinal] != tabela_verdade[elemento][sinal + 1] and sinal == len(tabela_verdade[elemento]) - 2:
                intervalo += f'{(sinal+1)*2}ns {tabela_verdade[elemento][sinal]} {((sinal+1)*2) + 0.1}ns {tabela_verdade[elemento][sinal + 1]}'

            elif tabela_verdade[elemento][sinal] != tabela_verdade[elemento][sinal + 1]:
                intervalo += f'{(sinal+1)*2}ns {tabela_verdade[elemento][sinal]} {((sinal+1)*2) + 0.1}ns {tabela_verdade[elemento][sinal + 1]} '

        intervalo += ')'
        pwls.append(intervalo)

    return pwls


def define_pwl_em_uso(pwls, fonte):
    global lista_de_linhas_arquivo_final

    for pwl in range(len(pwls)):
        if pwl == fonte:
            lista_de_linhas_arquivo_final.append(pwls[pwl])
        else:
            lista_de_linhas_arquivo_final.append(f'Vfonte{pwl} fonte{pwl} gnd PWL (0ns 0)')


def atrasos_measure(tabela_verdade, pwls):
    global lista_de_linhas_arquivo_final
    comando = f'.measure tran '
    atraso_tphl, atraso_tplh = '', ''

    for linha in range(len(tabela_verdade[0]) - 1):
        for linha_abaixo in range(linha + 1, len(tabela_verdade[0])):
            lista_de_linhas_arquivo_final = []
            alterou = 0
            fonte = None

            for sinal in range(len(tabela_verdade) - 1):
                if tabela_verdade[sinal][linha] != tabela_verdade[sinal][linha_abaixo]:
                    fonte = sinal
                    alterou += 1
            
            if alterou == 1 and tabela_verdade[-1][linha] != tabela_verdade[-1][linha_abaixo]:
                if tabela_verdade[-1][linha] == 1:
                    atraso_tphl = comando + f'tphl_l{linha}_l{linha_abaixo} trig v(fonte{fonte}) val=\'0.5*1\' rise=1 + targ v(saida) val=\'0.5*1\' fall=1'
                    atraso_tplh = comando + f'tplh_l{linha_abaixo}_l{linha} trig v(fonte{fonte}) val=\'0.5*1\' fall=1 + targ v(saida) val=\'0.5*1\' rise=1'
                
                elif tabela_verdade[-1][linha] == 0:
                    atraso_tplh = comando + f'tplh_l{linha_abaixo}_l{linha} trig v(fonte{fonte}) val=\'0.5*1\' rise=1 + targ v(saida) val=\'0.5*1\' fall=1'
                    atraso_tphl = comando + f'tphl_l{linha}_l{linha_abaixo} trig v(fonte{fonte}) val=\'0.5*1\' fall=1 + targ v(saida) val=\'0.5*1\' rise=1'

                arquivo = cria_arquivo_spice(f'atrasos_{linha}_{linha_abaixo}')

                define_pwl_em_uso(pwls, fonte)

                lista_de_linhas_arquivo_final.append('\n*DECLARAR O CIRCUITO\n\n*...\n')
                lista_de_linhas_arquivo_final.append('*SIMULACAO TRANSIENTE DE 32ns COM PASSO DE 0.1ns')
                lista_de_linhas_arquivo_final.append('.tran 0.1ns 32ns\n')
                lista_de_linhas_arquivo_final.append(atraso_tphl)
                lista_de_linhas_arquivo_final.append(atraso_tplh)
                lista_de_linhas_arquivo_final.append('\n*FIM DO ARQUIVO SPICE')
                lista_de_linhas_arquivo_final.append('.end')

                escreve_no_arquivo_spice(arquivo, lista_de_linhas_arquivo_final)


def main():
    global lista_de_linhas_arquivo_final

    _, string_hexadecimal = entrada_de_dados()

    string_binario = gera_binario(string_hexadecimal)

    log_fontes = define_numero_de_fontes(len(string_binario))

    tabela_verdade = gera_tabela_verdade(log_fontes, string_binario)

    lista_pwls = pwl(tabela_verdade)

    atrasos_measure(tabela_verdade, lista_pwls)

main()
