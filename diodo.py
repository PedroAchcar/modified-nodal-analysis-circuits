import numpy as np


Gn = np.zeros([2, 2])
In = np.zeros([2, 1])
# print(Gn, In, sep='\n\n')

#    nome, noA, noB,          Is,     nVt
D = ['D1', '1', '0', '10**(-15)', '0.025']
tensoes_iniciais = [0, 1]

Go = eval(D[3])*np.exp(tensoes_iniciais[eval(D[1])-eval(D[2])])/eval(D[4])
print(Go)
