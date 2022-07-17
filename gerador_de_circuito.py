import math
lista_de_linhas_arquivo_final = []


def entrada_de_dados():
    global lista_de_linhas_arquivo_final
    nome_circuito = input("Digite o nome do circuito: ")
    ini_string = "e0"

    # dados iniciais
    lista_de_linhas_arquivo_final.append(nome_circuito)
    lista_de_linhas_arquivo_final.append('\n*PARAMETROS')
    lista_de_linhas_arquivo_final.append('.include 32nm_HP.pm')
    lista_de_linhas_arquivo_final.append('\n*DECLARANDO FONTES DE TENSAO')
    lista_de_linhas_arquivo_final.append('Vvdd vdd gnd 1')
    lista_de_linhas_arquivo_final.append('\n*DECLARACAO DAS FONTES')

    return nome_circuito, ini_string


def gera_binario(dado_de_entrada):
    global lista_de_linhas_arquivo_final
    binario = bin(int(dado_de_entrada, 16))
    saida_tabela_verdade = f'{binario[2:]}'
    
    return saida_tabela_verdade


def cria_arquivo_spice(nome_circuito):
    arquivo = open(f'{nome_circuito}.txt', 'w+')

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
    for numero in range(numero_de_fontes):
        quantidade_de_zeros //= 2
        
        while len(coluna) < len(saida_tabela):
            for zero in range(quantidade_de_zeros):
                coluna.append(0)

            for um in range(quantidade_de_zeros):
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

def atrasos():
    pass


def main():
    global lista_de_linhas_arquivo_final

    nome, string_hexadecimal = entrada_de_dados()

    string_binario = gera_binario(string_hexadecimal)
    #print(string_binario)

    log_fontes = define_numero_de_fontes(len(string_binario))
    #print(log_fontes)

    tabela_verdade = gera_tabela_verdade(log_fontes, string_binario)
    #print(tabela_verdade)

    lista_pwls = pwl(tabela_verdade)
    
    lista_de_linhas_arquivo_final += lista_pwls

    lista_de_linhas_arquivo_final.append('\n*DECLARAR O CIRCUITO\n\n*...\n')
    lista_de_linhas_arquivo_final.append('*SIMULACAO TRANSIENTE DE 32ns COM PASSO DE 0.1ns')
    lista_de_linhas_arquivo_final.append('.tran 0.1ns 32ns\n')

    arquivo = cria_arquivo_spice(nome)

    escreve_no_arquivo_spice(arquivo, lista_de_linhas_arquivo_final)

main()