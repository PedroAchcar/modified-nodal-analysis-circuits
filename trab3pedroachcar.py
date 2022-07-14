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

def numeroNosCorrentes(netlist: list):
    '''Função que encontra quantos nós e correntes temos no circuito
    Entrada->netlist
    Saída->maior (int)'''
    maior = 0
    corrente = 0
    auxiliar = []
    for linha in netlist:
        item = linha.split(' ')
        if int(item[1]) > maior:
            maior = int(item[1])
        if int(item[2]) > maior:
            maior = int(item[2])
        if item[0][0] == 'E' or item[0][0] == 'F' or item[0][0] == 'G' or item[0][0] == 'H' or item[0][0] == 'K':
            if int(item[3]) > maior:
                maior = int(item[3])
            if int(item[4]) > maior:
                maior = int(item[4])
        if item[0][0] == 'E' or item[0][0] == 'F' or item[0][0] == 'V':
            corrente += 1
            auxiliar.append('j' + item[0])
        if item[0][0] == 'H':
            corrente += 2
            auxiliar.append('j1' + item[0])
            auxiliar.append('j2' + item[0])

    variaveis = list(range(1, maior+1))

    for i in range(maior):
        variaveis[i] = 'e' + str(variaveis[i])

    for i in auxiliar:
        variaveis.append(i)

    return maior, corrente, variaveis


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


def estampaFonteCorrenteIndependente(In: np.array, A: int, B: int, I: float) -> None:
    '''Altera In usando a estampa de uma fonte de corrente independente'''
    if A != 0:
        In[A-1] -= I
    if B != 0:
        In[B-1] += I


def estampaFonteCorrenteDependente(Gn: np.array, A: int, B: int,  C: int, D: int, Gm: float) -> None:
    '''Altera Gn usando a estampa de uma fonte de corrente dependente'''
    if A != 0 and C != 0:
        Gn[A-1, C-1] += Gm
    if A != 0 and D != 0:
        Gn[A-1, D-1] -= Gm
    if B != 0 and C != 0:
        Gn[B-1, C-1] -= Gm
    if B != 0 and D != 0:
        Gn[B-1, D-1] += Gm


def estampaFonteCorrenteAlternada(In: np.array, A: int, B: int, amplitude: float, frequencia: float, fase: float):
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


def estampaFonteTensao(Gn: np.array, In: np.array, A: int, B: int, x: int, V: float):
    '''Altera Gn usando a estampa de uma fonte de tensao DC'''
    In[x] -= V
    if A != 0:
        Gn[x, A-1] -= 1
        Gn[A-1, x] += 1
    if B != 0:
        Gn[x, B-1] += 1
        Gn[B-1, x] -= 1


def estampaAmpTensao(Gn: np.array, A: int, B: int, C: int, D: int, x: int, ganhoA: float):
    '''Altera Gn usando a estampa de um amplificador de tensao'''
    if A != 0:
        Gn[x, A-1] -= 1
        Gn[A-1, x] += 1
    if B != 0:
        Gn[x, B-1] += 1
        Gn[B-1, x] -= 1
    if C != 0:
        Gn[x, C-1] += ganhoA
    if D != 0:
        Gn[x, D-1] -= ganhoA


def estampaAmpCorrente(Gn: np.array, A: int, B: int, C: int, D: int, x: int, ganhoB: float):
    '''Altera Gn usando a estampa de um amplificador de corrente'''
    if A != 0:
        Gn[A-1, x] += ganhoB
    if B != 0:
        Gn[B-1, x] -= ganhoB
    if C != 0:
        Gn[C-1, x] += 1
        Gn[x, C-1] -= 1
    if D != 0:
        Gn[D-1, x] -= 1
        Gn[x, D-1] += 1


def estampaTransresistor(Gn: np.array, A: int, B: int, C: int, D: int, x: int, y: int, Rm: float):
    '''Altera Gn usando a estampa de um transresistor'''
    Gn[y, x] += Rm
    if A != 0:
        Gn[y, A-1] -= 1
        Gn[A-1, y] += 1
    if B != 0:
        Gn[y, B-1] += 1
        Gn[B-1, y] -= 1
    if C != 0:
        Gn[C-1, x] += 1
        Gn[x, C-1] -= 1
    if D != 0:
        Gn[D-1, x] -= 1
        Gn[x, D-1] += 1


def estampaFonteTensaoAlternada(Gn: np.array, In: np.array, A: int, B: int, x: int, amplitude: float, frequencia: float, fase: float):
    '''Altera Gn usando a estampa de uma fonte de tensao alternada'''
    pass


def estampador(netlist: list, Gn: np.array, In: np.array, variaveis: list):
    '''Aplica a estampa correspondente na matriz Gn ou no vetor In
        Saída->None or string'''
    for linha in netlist:
        item = linha.split(' ')
        if item[0][0] == 'R':
            estampaResistor(Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'C':
            estampaCapacitor(Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'L':
            estampaIndutor(Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'G':
            estampaFonteCorrenteDependente(Gn, int(item[1]), int(item[2]),
                                           int(item[3]), int(item[4]), float(item[5]))
        elif item[0][0] == 'K':
            estampaTransformador(Gn, int(item[1]), int(item[2]), int(item[3]),
                                 int(item[4]), float(item[5]), float(item[6]),
                                 float(item[7]))
        elif item[0][0] == 'E':
            estampaAmpTensao(Gn, int(item[1]), int(item[2]), int(item[3]),
                             int(item[4]), variaveis.index('j' + item[0]),
                             float(item[5]))
        elif item[0][0] == 'F':
            estampaAmpCorrente(Gn, int(item[1]), int(item[2]), int(item[3]),
                               int(item[4]), variaveis.index('j' + item[0]),
                               float(item[5]))
        elif item[0][0] == 'H':
            estampaTransresistor(Gn, int(item[1]), int(item[2]), int(item[3]),
                                 int(item[4]), variaveis.index('j1' + item[0]),
                                 variaveis.index('j2' + item[0]), float(item[5]))
        elif item[0][0] == 'I':
            if item[3][0] == 'D':
                estampaFonteCorrenteIndependente(
                    In, int(item[1]), int(item[2]), float(item[4]))
            elif item[3][0] == 'S':
                estampaFonteCorrenteAlternada(In, int(item[1]), int(item[2]),
                                              float(item[5]), float(item[6]),
                                              float(item[7]))
        elif item[0][0] == 'V':
            if item[3][0] == 'D':
                estampaFonteTensao(Gn, In, int(item[1]), int(item[2]),
                                   variaveis.index('j' + item[0]), float(item[4]))
            if item[3][0] == 'S':
                estampaFonteTensaoAlternada(In, int(item[1]), int(item[2]),
                                            variaveis.index('j' + item[0]),
                                            float(item[5]), float(item[6]), float(item[7]))
        else:
            return 'Netlist mal formulada.'


def main(txt='netlist.txt') -> None:
    '''Controla o programa chamando as funções devidas na ordem correspondente'''
    with open(txt, 'r') as txt:
        netlist = txt.readlines()
    netlist = limpaCodigo(netlist)
    maiorNo, correntes, variaveis = numeroNosCorrentes(netlist)
    Gn = gerarMatrizGn(maiorNo + correntes)
    In = gerarVetorIn(maiorNo + correntes)
    estampador(netlist, Gn, In, variaveis)

    solucao = np.round(np.linalg.solve(Gn, In), 3)

    print('-------------------------------------')
    print('Vetor solução:')
    for i in range(len(solucao)):
        print(f'{variaveis[i]} = {solucao[i][0]}')
    print('-------------------------------------')


if __name__ == '__main__':
    main()
