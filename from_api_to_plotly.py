import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import pprint
import sqlite3
import requests
import json
pp = pprint.PrettyPrinter()

coinsNewsURL = requests.get("https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=1d656ac0916147bf8d28e1dcda71266a")

coinsNews = coinsNewsURL.json() # this is a dictionary
#keys are: [u'status', u'articles', u'totalResults']

articles = coinsNews['articles']
keys = articles[0].keys() #[u'description',u'title', u'url', u'author', u'publishedAt', u'source', u'urlToImage']

articlesList = []
for i in range(0,len(articles)):
	article = []
	for j in range(0, 5):
		article.append(articles[i][keys[j]])
		#print i, j, article
	articlesList.append(article)

#create database
pp = pprint.PrettyPrinter()

conn = sqlite3.connect('cryptobase.db') #connection
c = conn.cursor()  #get a cursor object, all SQL commands are processed by it
#1st time only
c.execute('CREATE TABLE coinsNews(description TEXT, title TEXT, url TEXT, author TEXT, published TEXT)') #create a table
c.executemany('INSERT INTO coinsNews VALUES(?,?,?,?,?)', articlesList)

c.execute('SELECT * FROM coinsNews')
#pp.pprint(c.fetchall())

coinsRows = c.fetchall() 

#create visual in plotly
coinsList = []
for row in coinsRows:
	row = list(row)
	coinsList.append(row)

bitcoin = []
counts = []
count = 0
for row in coinsList:
	countBitcoin = 0
	for element in row:
		if "bitcoin" in element:
			countBitcoin +=1
	bitcoin.append(countBitcoin)
	count +=1
	counts.append(count)

trace = go.Scatter(x=[bitcoin] , y=[counts])
data = [trace]
py.iplot(data)



