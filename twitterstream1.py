

class TwitterAuth:
	# Go to http://dev.twitter.com and create an app. 
	# The consumer key and secret will be generated for you after
	consumer_key="oEbfCnZOoxWR5Wll4UbR2sK3b"
	consumer_secret="t93QnydyaLmU9lWtwtHFJp2wgrHfFq7Mh2raSrAh0o68WAUe4t"

	# After the step above, you will be redirected to your app's page.
	# Create an access token under the the "Your access token" section
	access_token="2612195366-uAZDYlV1TXgS3tsYBGv7zlRRLkGZo7ohJfpfa6j"
	access_token_secret="EYq3fGjtdY126NckjZNVVxqsg3SW7dHK4vcO3cvIasBGn"
	
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
#from auth import TwitterAuth

#Very simple (non-production) Twitter stream example
#1. Download / install python and tweepy (pip install tweepy)
#2. Fill in information in auth.py
#3. Run as: python streaming_simple.py
#4. It will keep running until the user presses ctrl+c to exit
#All output stored to output.json (one tweet  per line)
#Text of tweets also printed as recieved (see note about not doing this in production (final) code

class StdOutListener(StreamListener):
	
	#This function gets called every time a new tweet is received on the stream
	def on_data(self, data):
		#Just write data to one line in the file
		fhOut.write(data)
		
		#Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
		j=json.loads(data)

		#See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
		text=j["text"] #The text of the tweet
		coordinates =j["coordinates"] #coordinates of the tweet
		print(text, coordinates) #Print it out

	def on_error(self, status):
		print("ERROR")
		print(status)

if __name__ == '__main__':
	try:
		#Create a file to store output. "a" means append (add on to previous file)
		fhOut = open("output.json","a")

		#Create the listener
		l = StdOutListener()
		auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
		auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

		#Connect to the Twitter stream
		stream = Stream(auth, l)	

		#Terms to track
		stream.filter(track=["superbowl","patriots","sea hawks"])
		
		#Alternatively, location box  for geotagged tweets
		#stream.filter(locations=[-0.530, 51.322, 0.231, 51.707])

	except KeyboardInterrupt:
		#User pressed ctrl+c -- get ready to exit the program
		pass

	#Close the 
	fhOut.close()
