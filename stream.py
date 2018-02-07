#!/usr/bin/env python
# encoding: utf -8
import tweepy 
import json

# Authentication details. To obtain these visit dev.twitter.com
access_token = "252197958-qd0oMpuYd0VyB7Ghb0V3wzksS9heZkT3S2GfdSVs"
access_token_secret = "WK1ZNHalvvPsNVC2ogL5l6ojo8FwtMeXsYIvjWzakb8PA"
consumer_key = "vqusFEWFnnqEwqwXdAJnozuay"
consumer_secret =   "Dbc4mcepoUGDBuscEtF4YDUYV8MF9wBcUztH5eXI8AOAl6uIVv"

#This is the listener, responsible for recieving data
class StdOutListener(tweepy.StreamListener):
	def on_data(self,data):
		#parsing
		decoded=json.loads(data)
		#open a file to store the status objects
		file=open('stream.json', 'wb')
		#write json to file
		json.dump(decoded,file,sort_keys = True,indent=4)
		#show progress
		print "Writing tweets to file, CTRL + C to terminate the program"

		return True
	def on_error(self,status):
		print status
if __name__ =='__main__':
	l=StdOutListener()
	auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	#there are different kinds of streams
	stream=tweepy.Stream(auth,l)
	#Hashtag to stream
	stream.filter(track=["#cryptocurrency"])




