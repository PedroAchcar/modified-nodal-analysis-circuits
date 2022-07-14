import numpy as np
from math import cos, sin, radians, pi

w = 1


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
        if item[0][0] == 'G':
            if int(item[3]) > maior:
                maior = int(item[3])
            if int(item[4]) > maior:
                maior = int(item[4])
        if item[0][0] == 'K':
            if int(item[3]) > maior:
                maior = int(item[3])
            if int(item[4]) > maior:
                maior = int(item[4])
    return maior


def gerarMatrizGn(n: int):
    '''Gera a matriz Gn (nxn) composta de zeros pelo numpy
    Entrada->n
    Saída->Gn (np.array)'''
    Gn = np.zeros((n, n), 'complex')
    return Gn


def gerarVetorIn(n: int):
    '''Gera o vetor In (nx1) composto de zeros pelo numpy
    Entrada->n
    Saída->In (np.array)'''
    In = np.zeros((n, 1), 'complex')
    return In


def conversorRetangular(modulo: float, fase: float):
    '''Converte a fase e o modulo em numero retangular complexo (a+bj)'''
    a = modulo * cos(radians(fase))
    b = modulo * sin(radians(fase))
    return complex(a, b)


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


def estampaCapacitor(Gn: np.array, A: int, B: int, C: float) -> None:
    '''Altera Gn usando a estampa de um capacitor'''
    if A != 0:
        Gn[A-1, A-1] += w * C * 1j
    if B != 0:
        Gn[B-1, B-1] += w * C * 1j
    if A != 0 and B != 0:
        Gn[A-1, B-1] -= w * C * 1j
        Gn[B-1, A-1] -= w * C * 1j


def estampaIndutor(Gn: np.array, A: int, B: int, L: float) -> None:
    '''Altera Gn usando a estampa de um indutor'''
    if A != 0:
        Gn[A-1, A-1] += 1 / (w * L * 1j)
    if B != 0:
        Gn[B-1, B-1] += 1 / (w * L * 1j)
    if A != 0 and B != 0:
        Gn[A-1, B-1] -= 1 / (w * L * 1j)
        Gn[B-1, A-1] -= 1 / (w * L * 1j)


def estampaFonteIndependente(In: np.array, A: int, B: int, I: float) -> None:
    '''Altera In usando a estampa de uma fonte independente'''
    if A != 0:
        In[A-1] -= I
    if B != 0:
        In[B-1] += I


def estampaFonteDependente(Gn: np.array, A: int, B: int,  C: int, D: int, Gm: float) -> None:
    '''Altera Gn usando a estampa de uma fonte dependente'''
    if A != 0 and C != 0:
        Gn[A-1, C-1] += Gm
    if A != 0 and D != 0:
        Gn[A-1, D-1] -= Gm
    if B != 0 and C != 0:
        Gn[B-1, C-1] -= Gm
    if B != 0 and D != 0:
        Gn[B-1, D-1] += Gm


def estampaFonteAlternada(In: np.array, A: int, B: int, amplitude: float, frequencia: float, fase: float):
    '''Altera Gn usando a estampa de uma fonte alternada'''
    global w
    w = frequencia * 2 * pi
    if A != 0:
        In[A-1] -= conversorRetangular(amplitude, fase)
    if B != 0:
        In[B-1] += conversorRetangular(amplitude, fase)


def estampaTransformador(Gn: np.array, A: int, B: int, C: int, D: int, L1: float, L2: float, M: float) -> None:
    '''Altera Gn usando a estampa de um transformador'''
    gama11 = L2 / (L1*L2 - M**2)
    gama12 = -M / (L1*L2 - M**2)
    gama22 = L1 / (L1*L2 - M**2)
    if A != 0:
        Gn[A-1, A-1] += gama11 / (w*1j)
    if A != 0 and B != 0:
        Gn[A-1, B-1] -= gama11 / (w*1j)
        Gn[B-1, A-1] -= gama11 / (w*1j)
    if A != 0 and C != 0:
        Gn[A-1, C-1] += gama12 / (w*1j)
        Gn[C-1, A-1] += gama12 / (w*1j)
    if A != 0 and D != 0:
        Gn[A-1, D-1] -= gama12 / (w*1j)
        Gn[D-1, A-1] -= gama12 / (w*1j)
    if B != 0:
        Gn[B-1, B-1] += gama11 / (w*1j)
    if B != 0 and C != 0:
        Gn[B-1, C-1] -= gama12 / (w*1j)
        Gn[C-1, B-1] -= gama12 / (w*1j)
    if B != 0 and D != 0:
        Gn[B-1, D-1] += gama12 / (w*1j)
        Gn[D-1, B-1] += gama12 / (w*1j)
    if C != 0:
        Gn[C-1, C-1] += gama22 / (w*1j)
    if C != 0 and D != 0:
        Gn[C-1, D-1] -= gama22 / (w*1j)
        Gn[D-1, C-1] -= gama22 / (w*1j)
    if D != 0:
        Gn[D-1, D-1] += gama22 / (w*1j)


def estampador(netlist: list, Gn: np.array, In: np.array):
    '''Aplica a estampa correspondente na matriz Gn ou no vetor In
        Saída->None or string'''
    for linha in netlist:
        item = linha.split(' ')
        if item[0][0] == 'R':
            estampaResistor(
                Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'C':
            estampaCapacitor(Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'L':
            estampaIndutor(Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'I':
            if item[3][0] == 'D':
                estampaFonteIndependente(
                    In, int(item[1]), int(item[2]), float(item[4]))
            elif item[3][0] == 'S':
                estampaFonteAlternada(In, int(item[1]), int(item[2]), float(
                    item[5]), float(item[6]), float(item[7]))
        elif item[0][0] == 'G':
            estampaFonteDependente(Gn, int(item[1]), int(
                item[2]), int(item[3]), int(item[4]), float(item[5]))
        elif item[0][0] == 'K':
            estampaTransformador(Gn, int(item[1]), int(item[2]), int(item[3]), int(
                item[4]), float(item[5]), float(item[6]), float(item[7]))
        else:
            return 'Netlist mal formulada.'


def main(txt='netlist.txt'):
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
    return np.round(solucao, 3)


if __name__ == '__main__':
    print(main())
