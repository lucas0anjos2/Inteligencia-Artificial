import csv
import random


class bloco:
    def __init__(self, i):
        self.indice = i
        self.dados = list()


class knn:
    def __init__(self, arquivo):
        with open(arquivo, 'r') as dados:
            self.instanciaX = []
            self.teste = []
            self.treino = []
            registros = list(csv.reader(dados))
            registros = registros[1:-1]
            random.shuffle(registros)
            self.listaBlocos = []
            self.resultados = []
            self.raio = float()
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
                        self.listaBlocos[j].dados.append(registros[x])
                        contador += 1
            random.shuffle(self.listaBlocos)
            for z in range(len(self.listaBlocos)-1):
                self.treino.append(self.listaBlocos[z])
            self.teste = self.listaBlocos[-1]
            self.instanciaX = random.choice(self.treino)
            self.instanciaX = random.choice(self.instanciaX.dados)

    def distanciaEuclidiana(self,instancia1, instancia2):
        distancia = 0
        for i in range(1, 31): #OLHAR ISSO !!!
            distancia += (instancia1[i] - instancia2[i]) ** 2
        return distancia ** (1 / 2)

    def calcVizinhos(self, blocos, instancia, qtd):  # calculando vizinhos de uma instância
        distancias = []
        for i in range(len(blocos)):
            for j in range(len(blocos[i].dados)):
                distancia = self.distanciaEuclidiana(instancia, blocos[i].dados[j])
                if distancia == 0:
                    pass
                else:
                    distancias.append([blocos[i].dados[j], distancia])
            distancias.sort(key=lambda x: x[-1])
        vizinhos = []
        for i in range(qtd):
            vizinhos.append(distancias[i][-1])
        return vizinhos

    def treinar(self):
        vizinhos = self.calcVizinhos(self.treino, self.instanciaX, 100)
        self.raio = [min(vizinhos), max(vizinhos), sum(vizinhos) / vizinhos.__len__()]
        print(self.raio)
        return vizinhos

    def classificar(self):
        for i in range(len(self.teste.dados)):
            if self.distanciaEuclidiana(self.instanciaX, self.teste.dados[i]) < sum(self.raio)/3:
                self.resultados.append(self.teste.dados[i])

    def precisao(self):
        m = 0
        b = 0
        for i in range(len(self.resultados)):
            if self.resultados[i][0] == 'M':
                m += 1
            else:
                b += 1
        t = m+b
        m = (m / t ) * 100
        b = (b / t ) * 100
        print("Maligno: " + str(m))
        print("\n" + "Benigno: " + str(b))

def main():
    a = knn('cancer_breast.csv')
    a.treinar()
    a.classificar()
    a.precisao()
main()




