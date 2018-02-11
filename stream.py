#!/usr/bin/env python
# encoding: utf -8
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
from nltk.tokenize import word_tokenize
import re

access_token = "252197958-qd0oMpuYd0VyB7Ghb0V3wzksS9heZkT3S2GfdSVs"
access_secret = "WK1ZNHalvvPsNVC2ogL5l6ojo8FwtMeXsYIvjWzakb8PA"
consumer_key = "vqusFEWFnnqEwqwXdAJnozuay"
consumer_secret =   "Dbc4mcepoUGDBuscEtF4YDUYV8MF9wBcUztH5eXI8AOAl6uIVv"

auth=OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api=tweepy.API(auth)

#streaming the tweets

class MyListener(StreamListener):
	def on_data(self,data):
		try:
			with open('twitter.json','a') as f:
				f.write(data)
				return True
		except BaseException as e:
			print("Error on_data: %s" % str(e))
		return True

	def on_error(self,status):
		print(status)
		return True

twitter_stream=Stream(auth,MyListener())
twitter_stream.filter(track=['#cryptonews'])







#terms co-occurence

com=defaultdict(lambda : defaultdict(int))
with open(fname, 'r') as f:
	for line in f:
		tweet=json.loads(line)
		terms_only=[term for term in preprocess(tweet['text']) 
				if term not in stop 
				and not term.startswith(('#','@'))]
		for i in range(len(terms_only)-1):
			for j in range(i+1, len(terms_only)):
				w1,w2=sorted([terms_only[i],terms_only[j]])
				if w1 != w2:
					com[w1][w2] +=1
com_max=[]
#for each term, look for the most common co-occurences
for t1 in com:
	t1_max_terms=sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
	for t2,t2_count in t1_max_terms:
		com_max.append(((t1,t2), t2_count))
#get the most frequent co-occurences
terms_max=sorted(com_max, key=operator.itemgetter(1),  reverse=True)
#print(terms_max[:5])
