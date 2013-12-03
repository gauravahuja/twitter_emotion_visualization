#----------------------------------------------------------------------------#
# Imports.
#----------------------------------------------------------------------------#

import os
from flask import * # do not use '*'; actually input the dependencies.
import logging
from logging import Formatter, FileHandler
import json
import tweepy
from corpusHandler import *
from tweetHandler import *
import sys

consumer_key="FPqNv44c0qEbfcaW1Nw8g"
consumer_secret="1HBmN07H4oD2f7qtXgurb1dRc47lR84tU0E4WhhvM"
access_key = ""
access_token_secret = ""
auth = None
api = None

citiList = [('New Delhi',28.6,77.2), ('Mumbai',18.975,72.825833), ('Bangalore',12.983333,77.583333), ('New York',40.7141667,-74.0063889), ('Washington',38.8950000,-77.0366667), ('London',51.514125,-.093689), ('Toronto',43.666667,-79.416667), ('Sydney',-33.861481,151.205475), ('Vancouver',49.25,-123.133333), ('Paris',48.866667,2.333333), ('Seattle',47.6063889,-122.3308333)]

emotionDict = {'neutral':0, 0:'neutral','joy':1, 1:'joy', 'sadness':2, 2:'sadness', 'anger':3, 3:'anger', 'love':4, 4:'love', 'fear':5, 5:'fear', 'thankfulness':6, 6:'thankfulness', 'surprise':7, 7:'surprise'}
f = tweetFeatureExtractor(emotionDict)
cl = tweetClassifier(emotionDict)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def home():
	global api
	global auth
	if api == None:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		url = auth.get_authorization_url()
		session['request_token'] = (auth.request_token.key, auth.request_token.secret)
		return redirect(url)
	else:
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_key, access_token_secret)
		api = tweepy.API(auth, parser=tweepy.parsers.RawParser())
	return render_template('pages/index.html')

@app.route('/query',methods=['GET'])
def handleQuery():
	"""
	"""
	query = request.args
	qdict = {}
	for queryItem in query.iteritems():
		qdict[queryItem[0]] = queryItem[1]
	q = "Twitter"
	if qdict['q']:
		q = qdict['q']	
	s = getTweets(q)
	return json.dumps(s)

@app.route('/success',methods=['GET'])
def callback():
	query = request.args
	qdict = {}
	global api
	global auth
	global access_key
	global access_token_secret	
	for queryItem in query.iteritems():
		qdict[queryItem[0]] = queryItem[1]
	verifier = qdict['oauth_verifier']
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	token = session['request_token']
	del session['request_token']
	
	auth.set_request_token(token[0], token[1])
	auth.get_access_token(verifier)
	access_key = auth.access_token.key
	access_token_secret = auth.access_token.secret
	api = tweepy.API(auth, parser=tweepy.parsers.RawParser)	
	return redirect('/')
# Error handlers.

#@app.errorhandler(500)
#def internal_error(error):
    #db_session.rollback()
#    print '500'

@app.errorhandler(404)
def internal_error(error):
	return '404'

if not app.debug:
	file_handler = FileHandler('error.log')
	file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
	'[in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#----------------------------------------------------------------------------#
# Helping functions
#----------------------------------------------------------------------------#
def getTweets(query="Twitter"):
	"""
	"""
	global api
	result = []
	try:
		for i in range(len(citiList)):
			print citiList[i][0]
			lat = citiList[i][1]
			lg = citiList[i][2]
			g = "%f,%f,100mi" %(lat, lg)
			try:
				s = api.search(q=query, lang="en", geocode=g, result_type="mixed", rpp=20)
			except e:
				e = sys.exc_info()[0]
				print e
			#print "response %s" %(s)
			s = json.loads(s)
			tweets = s['statuses']
			tweet_result = []
			eCounts = [0.0]*8
			for tweet in tweets:
				tt = tweet['text']
				d= f.tweetExtract(tt)
				(ei, en) = cl.tweetClassify(d, 0.5)
				tweet_result.append([en, tt])
				eCounts[ei] += 1.0
			total = sum(eCounts)+1
			rd = {}
			rd['city'] = citiList[i][0]
			for i in range(8):
				rd[emotionDict[i]] = "%.2f" %(eCounts[i]*100/total)
			rd['tweets'] = tweet_result
			result.append(rd)
		return result
	except:
		return -1;
		
		
		
		
		
	
	
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
    
if __name__ == '__main__':

	cl.load('weights')
	# Specify port manually:
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	# Default port:
	#app.run()
