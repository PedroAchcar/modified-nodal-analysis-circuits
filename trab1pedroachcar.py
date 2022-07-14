import numpy as np


def limpaCodigo(netlist: list):
    '''Função que limpa o arquivo da netlist, removendo linhas em branco e comentários
    Entrada->netlist "suja"
    Saída->netlist "limpa"'''
    # Colocar na lista count quais sao os indices que precisam ser removidos
    count = []
    for i in range(len(netlist)):
        if netlist[i] == '\n' or netlist[i].startswith('*'):
            count.append(i)
    count.sort(reverse=True)

    # Remove os indices da netlist, teve que ser de tras para frente pois, ao remover
    # um indice, o que precisava ser removido tinha mudado de posicao na lista
    for i in count:
        netlist.pop(i)
    return netlist


def numeroNos(netlist: list):
    '''Função que encontra quantos nós temos no circuito
    Entrada->netlist
    Saída->maior (int)'''
    maior = 0
    for linha in netlist:
        item = linha.split(' ')
        if int(item[1]) > maior:
            maior = int(item[1])
        if int(item[2]) > maior:
            maior = int(item[2])
    return maior


def gerarMatrizGn(n: int):
    '''Gera a matriz Gn (nxn) composta de zeros pelo numpy
    Entrada->n
    Saída->Gn (np.array)'''
    Gn = np.zeros((n, n))
    return Gn


def gerarVetorIn(n: int):
    '''Gera o vetor In (nx1) composto de zeros pelo numpy
    Entrada->n
    Saída->In (np.array)'''
    In = np.zeros((n, 1))
    return In


def estampaResistor(Gn: np.array, A: int, B: int, R: float):
    '''Altera Gn usando a estampa de um resistor
    Entrada->Gn (np.array), A (int), B (int), R (float)
    Saída->None'''
    if A != 0:
        Gn[A-1, A-1] += 1/R
    if B != 0:
        Gn[B-1, B-1] += 1/R
    if A != 0 and B != 0:
        Gn[A-1, B-1] -= 1/R
        Gn[B-1, A-1] -= 1/R


def estampaFonteIndependente(In: np.array, A: int, B: int, I: float):
    '''Altera In usando a estampa de uma fonte independente
    Entrada->In (np.array), A (int), b (int), I (float)
    Saída->None'''
    if A != 0:
        In[A-1] -= I
    if B != 0:
        In[B-1] += I


def estampaFonteDependente(Gn: np.array, A: int, B: int,  C: int, D: int, Gm: float):
    '''Altera Gn usando a estampa de uma fonte dependente
    Entrada->Gn (np.array), A (int), B (int), C (int), D (int), R (float)
    Saída->None'''
    if A != 0 and C != 0:
        Gn[A-1, C-1] += Gm
    if A != 0 and D != 0:
        Gn[A-1, D-1] -= Gm
    if B != 0 and C != 0:
        Gn[B-1, C-1] -= Gm
    if B != 0 and D != 0:
        Gn[B-1, D-1] += Gm


def estampador(netlist: list, Gn: np.array, In: np.array):
    '''Aplica a estampa correspondente na matriz Gn ou no vetor In
    Entrada->netlist (list), Gn (np.array), In (np.array)
    Saída->None or string'''
    for linha in netlist:
        item = linha.split(' ')
        if item[0][0] == 'R':
            estampaResistor(
                Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'I':
            estampaFonteIndependente(
                In, int(item[1]), int(item[2]), float(item[4]))
        elif item[0][0] == 'G':
            estampaFonteDependente(Gn, int(item[1]), int(
                item[2]), int(item[3]), int(item[4]), float(item[5]))
        else:
            return 'Não é uma resistência nem fonte de corrente (in)dependente'


def main(txt):
    '''Controla o programa chamando as funções devidas na ordem correspondente
    Entrada->None
    Saída->solucao (np.array)'''
    with open(txt, 'r') as txt:
        netlist = txt.readlines()
    netlist = limpaCodigo(netlist)
    maiorNo = numeroNos(netlist)
    Gn = gerarMatrizGn(maiorNo)
    In = gerarVetorIn(maiorNo)
    estampador(netlist, Gn, In)

    solucao = np.linalg.solve(Gn, In)
    print('-----------------------')
    print('Vetor solução:')
    return solucao


if __name__ == '__main__':
    print(main('netlist.txt'))
