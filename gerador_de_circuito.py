
lista_de_linhas_arquivo_final = []


def entrada_de_dados():
    global lista_de_linhas_arquivo_final
    nome_circuito = input("Digite o nome do circuito")
    ini_string = "e0"

    return nome_circuito, ini_string


def gera_binario(dado_de_entrada):
    global lista_de_linhas_arquivo_final
    binario = bin(int(dado_de_entrada, 16))
    saida_tabela_verdade = f'{binario[2:]}'
    
    return saida_tabela_verdade


def cria_arquivo_spice(nome_circuito):
    global lista_de_linhas_arquivo_final
    arquivo = open(f'{nome_circuito}.txt', 'w+')
    
    # dados iniciais
    lista_de_linhas_arquivo_final.append(nome_circuito)
    lista_de_linhas_arquivo_final.append('.include 32nm_HP.pm')
    lista_de_linhas_arquivo_final.append('Vvdd vdd gnd 1')

    return arquivo


def escreve_no_arquivo_spice(arquivo, dados_para_o_arquivo):
    for item in dados_para_o_arquivo:
        arquivo.write(item)
        arquivo.write('\n')
    
    arquivo.close()


def gera_tabela_verdade(saida_tabela):



def pwl():
    pass


def atrasos():
    pass
