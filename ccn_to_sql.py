import pprint
import sqlite3
import requests

coinsNewsURL = requests.get(
    "https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=1d656ac0916147bf8d28e1dcda71266a")

coinsNews = coinsNewsURL.json()  # this is a dictionary
# keys are: [u'status', u'articles', u'totalResults']

articles = coinsNews['articles']
dicKeys = articles[0].keys() # [u'description',u'title', u'url', u'author', u'publishedAt', u'source', u'urlToImage']
keys = []
for element in dicKeys:
    if element != 'source':
        keys.append(element)

articlesList = []
colId = 0
for i in range(0, len(articles)):
    article = []
    article.append(colId)
    for j in range(0, 6):
        article.append(articles[i][keys[j]])
    # print i, j, article
    articlesList.append(article)
    colId +=1


# feed from website to sql table
conn = sqlite3.connect('cryptobase.db')  # connection
c = conn.cursor()
#c.execute('SELECT published FROM coinsNews WHERE id = (SELECT max(id) FROM coinsNews)')
c.execute('DROP TABLE coinsNews')
c.execute('CREATE TABLE coinsNews(id INTEGER, author TEXT, title TEXT, description TEXT, url TEXT, urlToImage TEXT, published TEXT)')
c.executemany('INSERT INTO coinsNews VALUES(?,?,?,?,?,?,?)', articlesList)
conn.commit()
