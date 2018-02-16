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


