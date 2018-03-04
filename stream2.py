import json
from nltk.tokenize import word_tokenize 
import re 
from collections import Counter 
import nltk 
from nltk.corpus import stopwords 
import string 
from nltk import bigrams 
import vincent 
import pandas 
from nltk.util import ngrams 
import matplotlib.pyplot as plt
import string
import numpy as np

#The purpose of this py file is to: pre-process the twitter data, count term frequencies, and visualize results.

#The commented text below can be used to check to see if the twitter data has successfully been uploaded in the json file and can be extracted.  It is also good to see how the data looks before you begin analysis and get familiar with the attributes
'''
data=json.loadwith open(open('twitter.json'))

fname='twitter.json'
with open('twitter.json', 'r') as f:
	line=f.readline() #read only the first tweet/line
	tweet=json.load(line) #load it as a Python dict
	print(json.dumps(tweet, indent=4)) #pretty-print

'''
#As Twitter data is unstructured and contains many things that are not words, they must be tokenized so that they are not included in our data that we will be mining.  There are common occurences in Tweets that must be omitted: emoticons, HTML tags, hashtag, @-mentions, URLS, numbers, etc.
emoticons_str=r"""
	(?:
		[:=;] #eyes
		[o0\-]? #nose
		[D\)\]\(\]/\\0pP] #mouth
	)"""
regex_str=[
	emoticons_str,
	r'<[^>]+>', #HTML tags
	r'(?:@[\w_]+)', # @mentions
	r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", #hashtags
	r'http[s]?://(?:[a-z][0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
	r'(?:(?:\d+,?)+(?:\.?\d+)?)', #numbers
	r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
	r'(?:[\w_]+)', #other words
	r'(?:\S)' #anything else
]
#regex_str is a list of possible patterns.  re.VERBOSE allows for ignoring spaces.  tokenize() puts all the tokens in a string and returns them as a list

tokens_re=re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re=re.compile(r'^'+emoticons_str+'$',re.VERBOSE| re.IGNORECASE)

def tokenize(s):
	return tokens_re.findall(s)

def preprocess(s, lowercase=False):
	tokens=tokenize(s)
	if lowercase:
		tokens=[token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens

#the following code checks to see if the above code was used to correctly take out the above terms from the text.  Tweet("text") is the variable in which the Twitter data is stored in the JSON file
	
with open('trial.json', 'r') as f:
	for line in f:		
		tweet=json.loads(line) #load it as a Python dict
		tokens=preprocess(tweet['text'])
		#print(preprocess(tweet['text']))

#the Counter() function is a term dictionary that counts frequecies and allows us to see the most common terms used
with open('trial.json', 'r') as f:
	
	count_all=Counter()
	for line in f:
		tweet=json.loads(line) #create a list with all the terms	
		terms_all=[term for term in preprocess(tweet['text'])] #update the counter	
		count_all.update(terms_all)
		#print the 5 most frequent words 
	#print(count_all.most_common(10))
	
#Using what we learned in class about removing words that are common in the English language but do not provide any insight into the usage of our hashtag, stopwords was included to get rid of such terms
#Terms that are common in Twitter language were added


with open('trial.json', 'r') as f:
	
	count_term=Counter()
	for line in f:
		tweet=json.loads(line) 

		punctuation=list(string.punctuation)
		stop=stopwords.words('english') + punctuation + ['rt', 'via', 'RT', ':', '1', 'contest', 'winner', 'referral', 'Retweet', '#bitcoin', '#Bitcoin', 'The', '...']
		terms_stop=[term for term in preprocess(tweet['text']) if term not in stop]
		
		#The code below is used to make our code more stringent on what we are analyzing

		terms_single=set(terms_all) #terms_single=count terms only once
		terms_hash=[term for term in preprocess(tweet['text']) #count hashtags only
			if term not in stop and
			term.startswith('#')]
		terms_only=[term for term in preprocess(tweet['text']) #count terms only ( no mentions)
			if term not in stop and
			not term.startswith(('@','u'))]
		
		count_term.update(terms_hash)
	#print(count_term.most_common(10))
#count_term.most_common(10))
#Using the code we leaned in class, we broke down usage of tuples commonly used together to see if that would provide us with any added insight



#to visualize the most common terms used, we put them in a histogram
word_freq=count_all.most_common(10)
labels, freq =zip(*word_freq)
data={'data': freq, 'x':labels}
bar=vincent.Bar(data,iter_idx='x')
bar.to_json('term_freq.json', html_out=True, html_path='chart.html')

#we also wanted to see how our chosen hashtag was used over time.  

bitcointags=[]
with open('bitcoin.json', 'r') as f:
	for line in f:
		tweet=json.loads(line) # as a Python dict
		terms_hash=[term for term in preprocess(tweet['text']) if term.startswith('#')] #look at '#' usage over time	
		if'#Bitcoin' in terms_hash:
			bitcointags.append(tweet['created_at']) #'created_at' is when the tweet was posted by the user
			
ones=[1]*len(bitcointags) #a list of "1" to count the hashtags
idx=pandas.DatetimeIndex(bitcointags) #the index of the series
bitcointag=pandas.Series(ones, index=idx) #the actual series 
per_minute=bitcointag.resample('1Min', how='sum').fillna(0) #tracking the frequency over time


ethereumtags=[]
with open('ethereum.json', 'r') as f:
	for line in f:
		tweet=json.loads(line) # as a Python dict
		terms_hash=[term for term in preprocess(tweet['text']) if term.startswith('#')] #look at '#' usage over time	
		if'#Ethereum' in terms_hash:
			bitcointags.append(tweet['created_at']) #'created_at' is when the tweet was posted by the user

ones=[1]*len(ethereumtags) #a list of "1" to count the hashtags
idx=pandas.DatetimeIndex(ethereumtags) #the index of the series
ethereumtag=pandas.Series(ones, index=idx) #the actual series 
per_minute2=ethereumtag.resample('1Min', how='sum').fillna(0) #tracking the frequency over time

'''
python_object=json.loads(open("bitcoin_chart.json").read())


#column one
axes=python_object['axes']
keys1=axes[0].keys()
keys=[]
for element in keys1:
	keys.append(element)

graphlist=[]

for i in range(len(axes)):
	graph=[]
	for j in range(0, len(keys)):
		graph.append(axes[i][keys[j]])
	graphlist.append(graph)
	#print(graphlist)

#column two
data=python_object['data']
keys2=data[0].keys()
keysb=[]
for element in keys2:
	keysb.append(element)

graphlist1=[]

for i in range(len(data)):
	graph1=[]
	for j in range(0, len(keysb)):
		graph1.append(data[i][keysb[j]])
	graphlist1.append(graph1)
	#print(graphlist1)

#column three
scales=python_object['scales']
keys3=scales[0].keys()
keysc=[]
for element in keys3:
	keysc.append(element)

graphlist2=[]

for i in range(len(scales)):
	graph2=[]
	for j in range(0,len(keysc)):
		if keysc[j]=='domain':
			graph2.append(scales[i][keysc[j]]['data'])
		elif keysc[j]=='field':
			graph2.append(scales[i][keysc[j]]['data'])
		else:
			graph2.append(scales[i][keysc[j]])
		graphlist2.append(graph2)
		print(graphlist2)
	
conn=sqlite3.connect('cryptobase.db')
c=conn.cursor()
c.execute('DROP TABLE python_object')
c.execute('CREATE TABLE python_object(scale TEXT, title INTERGER, type TEXT, name INTERGER, values INTERGER, height INTERGER, legends TEXT, marks TEXT, padding TEXT, scales INTERGER, width INTERGER)'  )
c.executemany('INSERT INTO python_object VALUES(?,?,?,?,?,?,?,?,?,?,?)', graphlist, graphlist1, graphlist2)
conn.commit()

'''
#graphing the usage over time
time_chart=vincent.Line(bitcointag)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('bitcoin_chart.json', html_out=True, html_path='bitcoin_chart.html')

#graphing the usage over time
time_chart=vincent.Line(ethereumtag)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('ethereum_chart.json', html_out=True, html_path='ethereum_chart.html')


both_data=dict(bitcointag=per_minute_i, ethereumtag=per_minute_s)
all_tags=pandas.DataFrame(data=both_data,
			index=per_minute_i.index )
all_tags=all_tags.resample('1Min', how='sum').fillna(0)

print(both_data)

stacked=vincent.StackedArea(both_data[['Bitcoin', 'Ethereum']])
stacked.axis_titles(x='Time', y='Freq')
stacked.legend(title='Twitter')
stacked.to_json('combined_chart.json', html_out=True, html_path='combined_chart.html')

time_chart=vincent.Line(both_data[['Bitcoin', 'Ethereum']])
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('combined_chart.json', html_out=True, html_path='combined_chart.html')


