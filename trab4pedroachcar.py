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
    Gn = np.zeros((n+1, n+1), 'complex')
    return Gn


def gerarVetorIn(n: int):
    '''Gera o vetor In (nx1) composto de zeros pelo numpy
    Entrada->n
    Saída->In (np.array)'''
    In = np.zeros((n+1, 1), 'complex')
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
    Gn[A, A] += 1/R
    Gn[A, B] -= 1/R
    Gn[B, A] -= 1/R
    Gn[B, B] += 1/R


# def estampaCapacitor(Gn: np.array, In: np.array, A: int, B: int, C: float, vc0: float) -> None:
#     '''Altera Gn usando a estampa de um capacitor'''
#     Gn[A, A] += w * C * 1j
#     Gn[A, B] -= w * C * 1j
#     Gn[B, A] -= w * C * 1j
#     Gn[B, B] += w * C * 1j

#     estampaFonteCorrenteIndependente(In, A, B, -C*vc0)

def estampaCapacitorTemporal(Gn: np.array, In: np.array, A: int, B: int, capacitancia: float, vt0: float, passo: float) -> None:
    pass


def estampaIndutor(Gn: np.array, In: np.array, A: int, B: int, L: float, il0: float) -> None:
    '''Altera Gn usando a estampa de um indutor'''
    Gn[A, A] += 1 / (w * L * 1j)
    Gn[A, B] -= 1 / (w * L * 1j)
    Gn[B, A] -= 1 / (w * L * 1j)
    Gn[B, B] += 1 / (w * L * 1j)

    estampaFonteCorrenteIndependente(In, A, B, il0/(w * 1j))


def estampaFonteCorrenteIndependente(In: np.array, A: int, B: int, I: float) -> None:
    '''Altera In usando a estampa de uma fonte de corrente independente'''
    In[A] -= I
    In[B] += I


def estampaFonteCorrenteAlternada(In: np.array, A: int, B: int, amplitude: float, frequencia: float, fase: float):
    '''Altera Gn usando a estampa de uma fonte de corrente alternada'''
    global w
    w = frequencia * 2 * pi
    In[A] -= conversorRetangular(amplitude, fase)
    In[B] += conversorRetangular(amplitude, fase)


def estampaFonteCorrenteDependente(Gn: np.array, A: int, B: int,  C: int, D: int, Gm: float) -> None:
    '''Altera Gn usando a estampa de uma fonte de corrente controlada por tensão'''
    Gn[A, C] += Gm
    Gn[A, D] -= Gm
    Gn[B, C] -= Gm
    Gn[B, D] += Gm


def estampaAmpCorrente(Gn: np.array, A: int, B: int, C: int, D: int, x: int, ganhoB: float):
    '''Altera Gn usando a estampa de uma fonte de corrente controlada por corrente'''
    Gn[A, x] += ganhoB
    Gn[B, x] -= ganhoB
    Gn[C, x] += 1
    Gn[D, x] -= 1
    Gn[x, C] -= 1
    Gn[x, D] += 1


def estampaFonteTensao(Gn: np.array, In: np.array, A: int, B: int, x: int, V: float):
    '''Altera Gn usando a estampa de uma fonte de tensão independente'''
    Gn[A, x] += 1
    Gn[B, x] -= 1
    Gn[x, A] -= 1
    Gn[x, B] += 1
    In[x] -= V


def estampaFonteTensaoAlternada(Gn: np.array, In: np.array, A: int, B: int, x: int, amplitude: float, frequencia: float, fase: float):
    '''Altera Gn usando a estampa de uma fonte de tensao alternada'''
    global w
    w = frequencia * 2 * pi
    Gn[A, x] += 1
    Gn[B, x] -= 1
    Gn[x, A] -= 1
    Gn[x, B] += 1
    In[x] -= conversorRetangular(amplitude, fase)


def estampaAmpTensao(Gn: np.array, A: int, B: int, C: int, D: int, x: int, ganhoA: float):
    '''Altera Gn usando a estampa de uma fonte de tensão controlada por tensão'''
    Gn[A, x] += 1
    Gn[B, x] -= 1
    Gn[x, A] -= 1
    Gn[x, B] += 1
    Gn[x, C] += ganhoA
    Gn[x, D] -= ganhoA


def estampaTransresistor(Gn: np.array, A: int, B: int, C: int, D: int, x: int, y: int, Rm: float):
    '''Altera Gn usando a estampa de uma fonte de tensão controlada por corrente'''
    Gn[A, y] += 1
    Gn[B, y] -= 1
    Gn[C, x] += 1
    Gn[D, x] -= 1
    Gn[x, C] -= 1
    Gn[x, D] += 1
    Gn[y, A] -= 1
    Gn[y, B] += 1
    Gn[y, x] += Rm


def estampaTransformador(Gn: np.array, A: int, B: int, C: int, D: int, L1: float, L2: float, M: float) -> None:
    '''Altera Gn usando a estampa de um transformador'''
    gama11 = L2 / (L1*L2 - M**2)
    gama12 = -M / (L1*L2 - M**2)
    # Sei que eh uma copia de linha, porem melhor para me localizar
    gama21 = -M / (L1*L2 - M**2)
    gama22 = L1 / (L1*L2 - M**2)

    Gn[A, A] += gama11 / (w*1j)
    Gn[A, B] -= gama11 / (w*1j)
    Gn[A, C] += gama12 / (w*1j)
    Gn[A, D] -= gama12 / (w*1j)
    Gn[B, A] -= gama11 / (w*1j)
    Gn[B, B] += gama11 / (w*1j)
    Gn[B, C] -= gama12 / (w*1j)
    Gn[B, D] += gama12 / (w*1j)
    Gn[C, A] += gama21 / (w*1j)
    Gn[C, B] -= gama21 / (w*1j)
    Gn[C, C] += gama22 / (w*1j)
    Gn[C, D] -= gama22 / (w*1j)
    Gn[D, A] -= gama21 / (w*1j)
    Gn[D, B] += gama21 / (w*1j)
    Gn[D, C] -= gama22 / (w*1j)
    Gn[D, D] += gama22 / (w*1j)


def estampaDiodo(Gn: np.array, In: np.array, A: int, B: int, Is: float, nVt: float, vn, epsilon: float, entradas: list) -> None:
    matrizG = np.zeros(np.shape(Gn))
    vetorI = np.zeros(np.shape(In))
    eA0 = entradas[A+1]
    eB0 = entradas[B+1]
    k = 0

    if A == 0:
        eA0 = 0
    if B == 0:
        eB0 = 0

    # while k < 100 or () > epsilon:

    exp = np.exp(vn/nVt)
    G0 = Is * exp / nVt
    I0 = Is * (exp - 1) - G0 * vn

    estampaResistor(matrizG, A, B, 1/G0)
    estampaFonteCorrenteIndependente(vetorI, A, B, I0)


def estampador(netlist: list, Gn: np.array, In: np.array, variaveis: list, passo: float, epsilon: float, entradas: list, num_pontos: int, resultados: np.array):
    '''Aplica a estampa correspondente na matriz Gn ou no vetor In
        Saída->None or string'''
    for atual in range(1, num_pontos):
        back = 0
        for k in range(100):
            matrizG =
    for linha in netlist:
        item = linha.split(' ')
        if item[0][0] == 'R':
            estampaResistor(Gn, int(item[1]), int(item[2]), float(item[3]))
        elif item[0][0] == 'C':
            # estampaCapacitor(Gn, In, int(item[1]), int(item[2]),
            #  float(item[3]), float(item[4]))
            estampaCapacitorTemporal(Gn, In, int(item[1]), int(item[2]),
                                     float(item[3]), float(item[4]), vt0, passo)
        elif item[0][0] == 'L':
            estampaIndutor(Gn, In, int(item[1]), int(item[2]),
                           float(item[3]), float(item[4]))
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
        elif item[0][0] == 'D':
            vn = ''
            estampaDiodo(Gn, In, int(item[1]), int(item[2]),
                         float(item[3]), float(item[4]), vn, epsilon, entradas)
        else:
            return 'Netlist mal formulada.'


def main(txt, tempo, passo, epsilon, entradas, saidas) -> None:
    '''Controla o programa chamando as funções devidas na ordem correspondente'''
    num_pontos = int(tempo/passo)

    with open(txt, 'r') as txt:
        netlist = txt.readlines()
    netlist = limpaCodigo(netlist)
    maiorNo, correntes, variaveis = numeroNosCorrentes(netlist)
    Gn = gerarMatrizGn(maiorNo + correntes)
    In = gerarVetorIn(maiorNo + correntes)
    resultados = np.zeros((num_pontos, maiorNo+correntes))
    aux = [maiorNo, correntes, variaveis, tempo, passo, epsilon, num_pontos]
    estampador(netlist, Gn, In, variaveis, passo, epsilon,
               entradas, saidas, num_pontos, resultados)
    #'''COLOCANDO COISAS NA LISTA AUX'''#

    Gn = Gn[1:, 1:]
    In = In[1:]
    # print(Gn)
    # print('-------------------------------')
    # print(In)
    # print('-------------------------------')

    solucao = np.round(np.linalg.solve(Gn, In), 3)

    return solucao


if __name__ == '__main__':
    print(main('netlist.txt'))


'''
TODO:
D
V SIN
I PULSE
V PULSE
'''
