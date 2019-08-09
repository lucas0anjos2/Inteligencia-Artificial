import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

arq = csv.reader(open('tweets_filtrados.csv', encoding="latin-1"))
tweets = pd.read_csv('tweets_filtrados.csv')
print(tweets.shape)
print(tweets.head())
x = tweets.drop('Sentimento', axis=1)
y = tweets['Sentimento']
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size = 0.20)
classificador = DecisionTreeClassifier(criterion = "gini", random_state = 100, max_depth = 3)
#classificador = classificador.fit(X_train, Y_train)
vectorizer = CountVectorizer()
treino = vectorizer.fit(X_train,Y_train)

treino1 = list()
for linha in arq:
    tf_vectorizer = TfidfVectorizer(use_idf=True)
    X = tf_vectorizer.fit_transform(linha)
print (treino1)

linhas = csv.reader(tweets)
dataSet = list(linhas)