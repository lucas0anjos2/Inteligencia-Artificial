import nltk
import unicodedata
from unicodedata import normalize
import re
import csv
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from unidecode import unidecode
iteracao = 0

def removerAcentos(lista):
    listaAux = []
    for w in lista:
        listaAux.append(normalize('NFKD', w).encode('ASCII', 'ignore').decode('ASCII'))
    return listaAux

def removeStopWords(texto):
    tokenizer = RegexpTokenizer(r'\w+')
    x = tokenizer.tokenize(texto)

    stopWords = set(stopwords.words('english'))

    wordsFiltered = []
    for w in x:
        if w not in stopWords:
            #print(w)
            wordsFiltered.append(w)

    listaAux = removerAcentos(wordsFiltered)
    #wordsFiltered = removerAcentos(wordsFiltered)

    return listaAux

def removeEmoji(lista):
    emojiFiltered = []
    for x in lista:
        if x.encode("utf-8"):
           emojiFiltered.append(x)
    return emojiFiltered

def removeUrl(texto):
    url_reg = r'[a-z]*[:.]+\S+'
    result = re.sub(url_reg, '', texto)
    return result

def removeNumeros(lista):
    #numberFiltered = []
    for x in lista:
        if re.sub('[^0-9]', '',  x):
            lista.remove(x)
    return lista

def stemming(texto):
    from nltk.stem import PorterStemmer
    x = []
    p = PorterStemmer()
    for i in texto:
        if len(i) <= 3:
            del i
        else:
            x.append(p.stem(i))
    return x

def lendoArquivoCsv():
    x = []
    global iteracao
    new_file = csv.reader(open('tweets.csv', encoding="latin-1"))
    for linha in new_file:
        x = removeUrl(linha[2])
        x = removeStopWords(x)
        x = removeEmoji(x)
        x = removeNumeros(x)
        #print(x)
        x = stemming(x)

        if len(x) == 1:
            del x
        else:
            #escrevendo no arquivo editado
            with open('tweets_filtrados.csv', 'a', newline='') as saida:
                escrever = csv.writer(saida)

                if iteracao == 0:
                    a = []
                    a = ["Sentimento", "Texto"]
                    escrever.writerow(a)
                    iteracao = iteracao + 1
                else:
                    documents = ' '.join(x)
                    sentimento = ''.join(linha[0])
                    lista = [sentimento, documents]
                    print(lista)
                    escrever.writerow(lista)

    saida.close()


#Chamada do método
lendoArquivoCsv()