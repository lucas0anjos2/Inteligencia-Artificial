import csv
import nltk
import re

from nltk.translate import metrics
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn import svm
from sklearn.metrics import accuracy_score
import pandas as pd

dataset = pd.read_csv('tweets_filtrados.csv')
dataset.count()

#separando os tweets das classes
y = dataset['Sentimento'].values
x = dataset['Texto'].values

#treinando usando svm
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.20)
vectorizer = CountVectorizer(analyzer="word")
freq_tweets = vectorizer.fit_transform(x)
modelo = svm
modelo.SVC(freq_tweets,y)

#Fazendo classificação
freq_testes = vectorizer.transform(X_test)
#modelo.fit(freq_tweets, y)

#resultados = cross_val_predict(modelo, freq_tweets, y, cv=10)
print(accuracy_score(Y_test, X_test))


