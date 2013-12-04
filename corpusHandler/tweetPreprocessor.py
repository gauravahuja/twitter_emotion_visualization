"""
Preprocess Tweets
"""
import os
import json
import logging
import re


class tweetPreprocessor:
	"""
	tweetPreprocessor Class
	"""	
	def __init__(self, tweetList_file, tweet_dir, output_file):
		"""
		Initializes the tweet preprocessor. Parameters:
			1. tweetList_file: File where each line specifies a tweet id and its emotion. eg "tweet_id emotion"
			2. tweet_dir: The path of the directory containing tweets. Each tweet is in a file <tweet_id>.json
			3. output_file: File to output preprocessed tweets. Format of output file "tweet id, emotion, preprocessed tweet"				 		
		"""
		self.logger = logging.getLogger("corpusHandler.tweetDownloader.%s" %(output_file))
		self.logger.setLevel(logging.DEBUG)
		self.tweetList_file = tweetList_file
		self.tweetDict = {}
		self.tweet_dir = tweet_dir
		self.output_file = output_file
		self.initialize()
	
	def initialize(self): 
		"""
		Internal Function. Used Internally
		"""
		f = open(self.tweetList_file)
		l = f.readline()
		while l:
			fields = l.strip().split()
			tweet_id = int(fields[0])
			emotion = fields[1]
			self.tweetDict[tweet_id] = emotion
			l = f.readline()
		f.close()
	
	def getTweetText(self, tweetFile):
		"""
		Gets the tweet text from a file containing tweet in json format. The tweetDownloader class downloads each tweet in json format. Parameters:
			1. tweetFile: File name of json file.
		
		return: tweet text
		rtype: string
		"""
		f =  open(tweetFile)
		tweet = json.load(f)
		f.close()
		tweet_text =  tweet.get('text', "")
		tweet_text = tweet_text.encode('ascii', 'replace')
		return tweet_text
	
	
	def preprocess_tweet(self,tweet_text):
		"""
		Preprocesses individual tweet. Handles hashtags, punctuations etc. Parameters:
			1. tweet_text: The tweet to be preprocessed
		return: preprocessed tweet text
		rtype : string
		"""
		tweet_text = tweet_text.replace('@', ' @')
		tweet_text = tweet_text.replace('#', ' ')
		tweet_text = tweet_text.replace(',', ' , ')
		tweet_text = tweet_text.replace('!', ' ! ')
		tweet_text = tweet_text.replace('?', ' ? ')
		tweet_text = tweet_text.replace('\'', ' \' ')
		tokens = tweet_text.split()		
		for i in range(len(tokens)):
			t = tokens[i]
			if t[0] == '@':
				t = "@user"
			tokens[i] = t
		tweet_text = " ".join(tokens)
		tweet_text = tweet_text.lower()
		return tweet_text
		
	def preprocess(self):
		"""
		Starts the preprocessing of all the tweet files in the tweet_dir and specified in tweetList_file and saves them to output_file. All these parameters are given while creating an object of this class.
		"""
		tweet_files = os.listdir(self.tweet_dir)
		f = open(self.output_file, 'w')
		for tweet_file in tweet_files:
			fields = tweet_file.split('.')
			if "json" not in fields[-1]:
				continue
			tweet_id = int(fields[0])
			if self.tweetDict.get(tweet_id, -1) == -1:
				continue
			emotion = self.tweetDict[tweet_id]
			tweet_text = self.getTweetText(self.tweet_dir + '/' + tweet_file)
			if tweet_text == "":
				self.logger.error("No text in file %s" %(tweet_file))			
			p_tweet_text = self.preprocess_tweet(tweet_text)
			s = "%d, %s, %s\n" %(tweet_id, emotion, p_tweet_text)
			f.write(s)
		f.close()
			
			
