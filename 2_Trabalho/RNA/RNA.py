import csv
import random

class bloco:
    def __init__(self, i):
        self.indice = i
        self.dados = list()

class RNA:
    def __init__(self, arquivo):
        with open(arquivo, 'r') as dados:
            self.w = []
            self.n = 1
            self.bias = 1
            self.wBias = 0
            self.teste = []
            self.treino = []
            registros = list(csv.reader(dados))
            self.listaBlocos = []
            self.resultados = []
            for i in range(1,len(registros)):
                for j in range(1,31):
                    registros[i][j] = float(registros[i][j])
            for i in range(10): # inicializando lista de blocos
                b = bloco(i)
                self.listaBlocos.append(b)
            j = 0 # indice para listaBlocos
            contador = 0
            # dividindo amostra de registros: 569 registros
            #   9 blocos com 57 = 513
            #   1 bloco com 56
            #   513 + 56 = 569
            for x in range(1,len(registros)):
                if j < 9:
                    if contador < 56:
                        self.listaBlocos[j].dados.append(registros[x])
                        contador += 1
                    else:
                        self.listaBlocos[j].dados.append(registros[x])
                        contador = 0
                        j += 1
                if j == 9:
                    if contador < 56:
                        self.listaBlocos[j].dados.append(registros[x+1])
                        contador += 1
            random.shuffle(self.listaBlocos)
            for z in range(len(self.listaBlocos)-1):
                self.treino.append(self.listaBlocos[z])
            self.teste = self.listaBlocos[-1]
            for i in range(30):
                self.w.append(0)

    # x é uma linha do csv
    def somador(self, x):
        u = 0
        for i in range(1,31):
            u += x[i] * self.w[i-1]
        u += self.bias * self.wBias
        return u

    def degrau(self, u):
        if u < 0: return 0
        else: return 1
    # B = 1, M = 0
    def erro(self, x, y):
        yd = 0
        if x[0] == "B": yd = 1
        return yd - y

    #atualiza pesos e Bias para um valor de x
    def aprendizado(self, x):
        novoW = []
        u = self.somador(x)
        y = self.degrau(u)
        erro = self.erro(x, y)
        for i in range(len(self.w)):
            fator = self.n * erro * x[i+1]
            novoW.append(self.w[i] + (self.n * fator))
        self.wBias += self.n * erro * self.bias
        self.w = novoW


    def treinar(self):
        for i in range(len(self.treino)):
            for j in range(len(self.treino[i].dados)):
                self.aprendizado(self.treino[i].dados[j])

    def testar(self):
        resultado = []
        for i in range(len(self.teste.dados)):
            u = self.somador(self.teste.dados[i])
            y = self.degrau(u)
            erro = self.erro(self.teste.dados[i], y)
            resultado.append(erro)
        return resultado




def main():
    a = RNA("cancer_breast.csv")
    # as épocas podem ser variadas
    for i in range(10):
        a.treinar()
    print(a.w)
    r = a.testar()
    a, e = 0,0
    for i in range(len(r)):
        if r[i] == 1: e += 1
        elif r[i] == 0: a += 1
    print("acerto = " + str(a / (a + e)))
    print("erro = " + str(e / (a + e)))




main()

