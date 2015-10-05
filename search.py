try:
    import json
except ImportError:
    import simplejson as json
import urllib2
import urllib
import codecs
import time
import datetime
import os
import random
import time
import tweepy
from tweepy.parsers import RawParser
import sys
#import cld

fhLog = codecs.open("LOG.txt",'a','UTF-8')
def logPrint(s):
	fhLog.write("%s\n"%s)
	print s

#Update this line with the terms you want to search for
terms =  ["#acctourney"]


class TwitterAuth:
	# Go to http://dev.twitter.com and create an app. 
	# The consumer key and secret will be generated for you after
	consumer_key="oEbfCnZOoxWR5Wll4UbR2sK3b"
	consumer_secret="t93QnydyaLmU9lWtwtHFJp2wgrHfFq7Mh2raSrAh0o68WAUe4t"

	# After the step above, you will be redirected to your app's page.
	# Create an access token under the the "Your access token" section
	access_token="2612195366-uAZDYlV1TXgS3tsYBGv7zlRRLkGZo7ohJfpfa6j"
	access_token_secret="EYq3fGjtdY126NckjZNVVxqsg3SW7dHK4vcO3cvIasBGn"

auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

rawParser = RawParser()
api = tweepy.API(auth_handler=auth, parser=rawParser)

fhOverall=None
allTweets = {}

termCnt=0
for term in terms:
	termCnt+=1
	logPrint("Getting term %s (%s of %s)"%(term,termCnt,len(terms)))
	minid= "5651531452699402294" #Lowest id we've seen so far, start at None
	count=1
	while True:
		try:
			fh=open("output/"+term+"_" + str(count) + ".json","r")
			result=fh.read()
			fh.close()
			wait=0
		except:	
			if minid==None:
				result=api.search(count=100,q=term,result_type="recent")
			else:
				result=api.search(count=100,q=term,max_id=minid,result_type="recent")
			#The following will produce errors if the filesystem doesn't support characters used in the search term! (also above in try block)
			fh=open("output/"+term+"_" + str(count) + ".json","w")
			fh.write(result)
			fh.close()
			wait=5
			
		result=json.loads(result)
		if "statuses" in result and len(result["statuses"])>0:
			logPrint("\nThere are %s results."%len(result["statuses"]))
			for status in result["statuses"]:
				if minid==None or status["id"]<minid:
					minid=status["id"]
			count+=1
			logPrint("Another page to get. Minimum id is %s"%minid)
		else:
			minid=None
			break
		
		#Deal with slight bug, if <=1 also quit
		if "statuses" in result and len(result["statuses"])<=1:
			minid=None
			break

		
		time.sleep(wait)

logPrint("\nDONE! Completed Successfully")
fhLog.close()