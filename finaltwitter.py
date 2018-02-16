import json
from nltk.tokenize import word_tokenize
import re
import operator 
import pandas as pd
import numpy as np
from collections import Counter
from nltk.corpus import stopwords
import string
from nltk import bigrams
from collections import defaultdict
import vincent
import pandas
import nltk
from nltk import word_tokenize 
from nltk.util import ngrams 
from datetime import datetime


with open('twitter.json', 'r') as f:
	line=f.readline() #read only the first tweet/line
	tweet=json.loads(line) #load it as a Python dict
	#rint(json.dumps(tweet, indent=4)) #pretty-print
	

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
tokens_re=re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re=re.compile(r'^'+emoticons_str+'$',re.VERBOSE| re.IGNORECASE)

def tokenize(s):
	return tokens_re.findall(s)

def preprocess(s, lowercase=False):
	tokens=tokenize(s)
	if lowercase:
		tokens=[token if emoticon_re.search(token) else token.lower() for token in tokens]
	return tokens


with open('twitter.json', 'r') as f:
	line=f.readline() #read only the first tweet/line
	tweet=json.loads(line) #load it as a Python dict
	#rint(tweet)
	tokens=preprocess(tweet['text'])



with open('twitter.json', 'r') as f:
	line=f.readline() 
	count_all=Counter()
	
	tweet=json.loads(line)
		#create a list with all the terms
	terms_all=[term for term in preprocess(tweet['text'])]
		#update the counter
	count_all.update(terms_all)
	#print the 5 most frequent words
#print(count_all.most_common(5))

#remove stopwords

punctuation=list(string.punctuation)
#rint(punctuation)
stop=stopwords.words('english') + punctuation + ['rt', 'via', 'RT', ['0-9'], ':', '1', 'contest', 'winner', 'referral', 'Retweet']
#int(type(stop))
#rint(stop)
terms_stop=[term for term in preprocess(tweet['text']) if term not in stop]
#rint(terms_stop)

  

#count terms only once

terms_single=set(terms_all)
#rint(terms_single)
#count hashtags only
terms_hash=[term for term in preprocess(tweet['text'])
	if term.startswith('#')]
#rint('real terms_hash', terms_hash)
#count terms only (no hashtags, no mentions
terms_only=[term for term in preprocess(tweet['text'])
	if term not in stop and
	not term.startswith(('#','@'))]
#rint('terms hash', terms_only)


with open('twitter.json', 'r') as f:
	line=f.readline() #read only the first tweet/line
	tweet=json.loads(line) #load it as a Python dict
	count_all=Counter()
	for line in f:
		
		#create a list with all the terms
		terms_only=[term for term in preprocess(tweet['text'])
			if term not in stop and
			not term.startswith(('#','@'))]
		#update the counter
		count_all.update(terms_only)
		
	#rint(count_only.most_common(10))


com=defaultdict(lambda :defaultdict(int))

token = nltk.word_tokenize(tweet['text'])
bigrams = ngrams(token,2)
trigrams = ngrams(token,3)
fourgrams = ngrams(token,4)
fivegrams = ngrams(token,5)
#rint Counter(bigrams)
#rint Counter(trigrams)
#rint Counter(fourgrams)
#rint Counter(fivegrams)



word_freq=count_all.most_common(20)
labels, freq =zip(*word_freq)
data={'data': freq, 'x':labels}
bar=vincent.Bar(data,iter_idx='x')
bar.to_json('term_freq.json', html_out=True, html_path='chart.html')


bitcointags=[]


with open('twitter.json', 'r') as f:
	#ine=f.readline() #read only the first tweet/line
	#weet=json.loads(line) #load it as a Python dict

	for line in f:
		tweet=json.loads(line) # as a Python dict
	
		terms_hash=[term for term in preprocess(tweet['text']) if term.startswith('#')]
			#rint(terms_hash)
			#track when the hashtag is mentioned
	
		if'#Bitcoin' in terms_hash:
			bitcointags.append(tweet['created_at'])
			#rint('this better work', bitcointags)
			print(tweet['created_at'])
		

	#a list of "1" to count the hashtags
ones=[1]*len(bitcointags)
#the index of the series
idx=pandas.DatetimeIndex(bitcointags)

#the actual series 
bitcointag=pandas.Series(ones, index=idx)
#rint(len(bitcointag))

#rint(bitcointag)
#bucketing
per_minute=bitcointag.resample('1Min', how='sum').fillna(0)

#rint(per_minute[:5])
time_chart=vincent.Line(per_minute)
time_chart.axis_titles(x='Time', y='Freq')
time_chart.to_json('time_chart.json', html_out=True, html_path='time_chart.html')





