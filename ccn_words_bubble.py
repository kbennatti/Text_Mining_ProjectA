from __future__ import division
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import pprint
import sqlite3
import plotly
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
import math
import random as rand


pp = pprint.PrettyPrinter()

# get table from database
def tableFromDatabase(database, table):
    conn = sqlite3.connect(database)  # connection
    c = conn.cursor()  # get a cursor object, all SQL commands are processed by
    c.execute('SELECT * FROM %s' % table)
    tableRows = c.fetchall()
    return tableRows

rows = tableFromDatabase('cryptobase.db', 'coinsNews')

# pass sql table to python list
coinsList = [list(row) for row in rows]

# normalize words
stop_words = set(stopwords.words('english') + ['cryptocurrency', 'cryptocurrencies', 'u', '000'])
lemmatizer = WordNetLemmatizer()
ps = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+') # takes only alphanum characters


normalized = []
counts = []
for row in coinsList:
    word_tokens = tokenizer.tokenize(row[2])
    word_lower = [w.lower() for w in word_tokens]
    word_stem = [lemmatizer.lemmatize(w) for w in word_lower]
    filtered_row = [w for w in word_stem if not w in stop_words]
    normalized.append(filtered_row)
    counts.append(Counter(filtered_row))

allWords = []
for row in normalized:
    for word in row:
        allWords.append(word)
countsWords = Counter(allWords)

# calculate tf-idf
def inverse_freq(all_documents):
    idf_values = {}
    all_tokens_set = set([item for row in all_documents for item in row])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, all_documents)
        idf_values[tkn] = math.log(len(all_documents) / (sum(contains_token)))
    return idf_values

#def tfidf(term, all_documents):
idf = inverse_freq(normalized)
tfidfs = {}
for term in idf:
       tfidf = idf[term]*countsWords[term]
       tfidfs[term]=tfidf

sortedTfidfs = sorted(tfidfs.items(), key=lambda x:x[1], reverse = True)
sortVal = sorted(tfidfs.values(), reverse=True)
sortKey = sorted(tfidfs, key=tfidfs.get, reverse=True)
topVal = sortVal[:20]
topKey = sortKey[:20]

# create bubble chart
plotly.tools.set_credentials_file(username='kalidurge', api_key='XA6wRnImtNkMVWtLKilG') #update api key every time
#randomly place x and y values on plot

x = [10,10,10,5,15,5,15,5,15,7.2,12.7,7.2,2.5,17.5,17.5,12.5,12.5,7.5,12.5,7.5]#[5, 6, 7, 8, 9, 10, 11, 12, 0, 1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19]#[x for x in range(0,20)] #np.array([rand.randrange(0,40) for x in range(0, len(topVal))])
y = [10,16,4,10,10,5,5,15,15,2.5,2.5,17.5,11.8,12.5,7.5,12.5,18,8,8,12.5] #np.array([rand.randrange(0,20) for y in range(0, len(topVal))])
color = sorted(np.random.randn(len(topVal)), reverse=True)

trace1 = go.Scatter(
    x=x,
    y=y,
    text=topKey,
    mode='markers+text',
    marker=dict(color=color, size=topVal, sizemode='area', sizeref=2.*max(topVal)/(150.**2)))

data = [trace1]
layout = go.Layout(title='Today\'s Top 20 Words Based on TF-IDF', titlefont=dict(
            size=32),    xaxis=dict(
        title='Source: Crypto Coins News (www.ccn.com) API: https://newsapi.org/v2/everything?sources=crypto-coins-news&apiKey=1d656ac0916147bf8d28e1dcda71266a',
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    ),
    yaxis=dict(
        autorange=True,
        showgrid=False,
        zeroline=False,
        showline=False,
        autotick=True,
        ticks='',
        showticklabels=False
    ))
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='bubblechart-size')#change to iplot if running within ipython


