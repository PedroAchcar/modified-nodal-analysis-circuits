import numpy as np
import math
import matplotlib.pyplot as plt

# Recebe um (string)arquivo de netlist, e retorna as linhas não nulas do arquivo lido.


def lerArquivo(arquivo):
    file = open(arquivo)
    netlist = file.readlines()
    file.close()
    # Checar se o arquivo tem linhas vazias
    for i in netlist:
        if i == "\n":
            netlist.remove(i)
    return netlist

# Recebe um (string)arquivo de netlist, e retorna o maior número de nó encontrado, o numero de correntes de controle e o os nomes das icomatrizGnitas.


def contarNosCorrentes(netlist):
    contadorNo = 0
    contadorCorrente = 0
    aux = []
    for linha in netlist:
        #linha = valores.split()
        if(contadorNo <= int(linha[1])):
            contadorNo = int(linha[1])
        if(contadorNo <= int(linha[2])):
            contadorNo = int(linha[2])
        if((linha[0][0] == 'K') or (linha[0][0] == 'G') or (linha[0][0] == 'F') or (linha[0][0] == 'E') or (linha[0][0] == 'H')):
            if(contadorNo <= int(linha[3])):
                contadorNo = int(linha[3])
            if(contadorNo <= int(linha[4])):
                contadorNo = int(linha[4])
        if((linha[0][0] == 'V') or (linha[0][0] == 'E') or (linha[0][0] == 'F')):
            contadorCorrente += 1
            aux.append('j'+linha[0])
        if(linha[0][0] == 'H'):
            contadorCorrente += 2
            aux.append('j1'+linha[0])
            aux.append('j2'+linha[0])

    icomatrizGnitas = list(range(1, contadorNo+1))
    for i in range(contadorNo):
        icomatrizGnitas[i] = 'e'+str(icomatrizGnitas[i])
    for i in aux:
        icomatrizGnitas.append(i)
    return contadorNo, contadorCorrente, icomatrizGnitas


# Recebe um (int)n e retorna uma matriz nula tamanho n x n.
def gerarMatriz(n):
    return np.zeros((n, n), dtype='complex_')

# Recebe um (int)n e retorna um vetor nulo tamanho n x 1.


def gerarVetor(n):
    return np.zeros((n, 1), dtype='complex_')


def estamparDiodo(matrizGn, vetorIn, noA, noB, Is, nVt, vn):
    #G0 = (Is*math.e**(vn/nVt))/nVt
    #I0 = Is*(math.e**((vn/nVt)-1))-G0*vn
    exponential = np.exp(vn/nVt)
    G0 = Is * exponential / nVt
    I0 = Is * (exponential - 1) - G0 * vn
    # Resistor G0
    estamparResistor(matrizGn, noA, noB, 1/G0)
    # Fonte de corrente I0
    estamparFonteCorrente(vetorIn, noA, noB, I0)

# Recebe uma (array)matrizGn,(int)noA,(int)noB,(float)R e altera a matriz com a estampa de resistor.


def estamparResistor(matrizGn, noA, noB, R):
    if (noA != 0):
        matrizGn[noA, noA] += 1/R
    if (noB != 0):
        matrizGn[noB, noB] += 1/R
    if (noB != 0 and noA != 0):
        matrizGn[noA, noB] += -1/R
        matrizGn[noB, noA] += -1/R

# Recebe uma (array)vetorIn,(int)noA,(int)noB,(float)I e altera o vetor com a estampa de fonte de corrente DC.


def estamparFonteCorrente(vetorIn, noA, noB, I):
    if (noA != 0):
        vetorIn[noA] += - I
    if (noB != 0):
        vetorIn[noB] += I

# Recebe uma (array)vetorIn,(int)noA,(int)noB,(int)x,(float)A, (float)freq, (float)fase e altera o vetor com a estampa de fonte de tensao alternada.


def estamparFonteTensaoAlternadaTempo(matrizGn, vetorIn, noA, noB, DC, A, freq, fase, x, t):
    global w
    w = freq*2*math.pi
    phase = fase*math.pi/180
    vetorIn[x] += -(DC + A * math.cos(w*t + phase+math.pi/2))
    if (noA != 0):
        matrizGn[x, noA] += -1
        matrizGn[noA, x] += 1
    if (noB != 0):
        matrizGn[x, noB] += 1
        matrizGn[noB, x] += -1

# Recebe uma (array)matrizGn,(int)noA,(int)noB,(float)C e altera a matriz com a estampa de capacitor.
# Se houver condição inicial, estampa a fonte de corrente no vetorIn.


def estamparCapacitorTempo(matrizGn, vetorIn, noA, noB, C, it0, vt0, dt):
    trapezio = (2*C/dt) * vt0 + it0

    # fonte de corrente referente a condição inicial
    estamparFonteCorrente(vetorIn, noA, noB, trapezio)
    if (noA != 0):
        matrizGn[noA, noA] += 2*C/dt
    if (noB != 0):
        matrizGn[noB, noB] += 2*C/dt
    if (noB != 0 and noA != 0):
        matrizGn[noA, noB] += -2*C/dt
        matrizGn[noB, noA] += -2*C/dt

# Recebe um (array)matrizGn,(array)vetorIn que formam o sistema linear e retorna sua solução.


def resolverMatriz(matrizGn, vetorIn):
    return np.linalg.solve(matrizGn, vetorIn)


def trabalho(arquivo="netlist.txt", t=1, dt=0.001, epsilon=0.001):
    netlist = lerArquivo(arquivo)
    nPontos = int(t/dt)
    vc = np.zeros(nPontos)
    ic = np.zeros(nPontos)
    c = 0

    for i in range(len(netlist)):
        netlist[i] = netlist[i].split()

    print(netlist)

    # Conta nós e correntes de controle
    icognitas = contarNosCorrentes(netlist)
    numeroNos = icognitas[0]  # Pega apenas o numero de nos
    numeroCorrentes = icognitas[1]  # Pega apenas o numero de correntes
    icognitas = icognitas[2]  # Pega apenas os nomes das icomatrizGnitas
    matrizGn = gerarMatriz(numeroNos+numeroCorrentes)  # Cria a matrize Gn nula
    vetorIn = gerarVetor(numeroNos+numeroCorrentes)  # Cria o vetor In nulo
    # Cria vetor de resultados
    resultados = np.zeros((nPontos, numeroNos + numeroCorrentes))

    for atual in range(1, nPontos):
        anterior = 0
        for rodada in range(30):
            matrizGn = np.zeros(
                (numeroNos+1+numeroCorrentes, numeroNos+1+numeroCorrentes))
            vetorIn = np.zeros(numeroNos+1+numeroCorrentes)
            t = atual * dt
            actualCurrent = 1
            for i in range(len(netlist)):
                aux = netlist[i]

                if(aux[0][0] == 'D'):
                    if rodada == 0:
                        vn = np.random.rand()
                    else:
                        vn = anterior[int(aux[1])-1] - anterior[int(aux[2])-1]
                    estamparDiodo(matrizGn, vetorIn, int(aux[1]), int(
                        aux[2]), float(aux[3]), float(aux[4]), vn)

                elif(aux[0][0] == 'R'):
                    estamparResistor(matrizGn, int(aux[1]), int(
                        aux[2]), np.double(float(aux[3])))

                elif(aux[0][0] == 'V'):
                    estamparFonteTensaoAlternadaTempo(matrizGn, vetorIn, int(aux[1]), int(aux[2]), float(
                        aux[4]), float(aux[5]), float(aux[6]), float(aux[7]), numeroNos + actualCurrent, t)
                    actualCurrent += 1

                elif(aux[0][0] == 'C'):
                    estamparCapacitorTempo(matrizGn, vetorIn, int(aux[1]), int(
                        aux[2]), float(aux[3]), ic[atual - 1], vc[atual - 1], dt)

            matrizGn = matrizGn[1:, 1:]
            vetorIn = vetorIn[1:]

            e = resolverMatriz(matrizGn, vetorIn)

            if rodada > 1:
                if abs(e[0] - anterior[0]) < epsilon and abs(e[1] - anterior[1]) < epsilon:
                    break
            anterior = e
        if c != 0:
            vc[atual] = e[1]
            ic[atual] = e[1]*2*c[3]/dt-((2*c[3]/dt)*vc[atual-1]+ic[atual - 1])
        resultados[atual] = e

    e1 = [i[0] for i in resultados]
    e2 = [i[1] for i in resultados]

    tempo = [dt * i for i in range(nPontos)]

    plt.plot(tempo, e1)
    plt.plot(tempo, e2)
    plt.show()
    plt.close()


trabalho("netlist.txt", 3, 0.0005, 0.01)
