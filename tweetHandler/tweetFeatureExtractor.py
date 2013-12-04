"""
Tweet Feature extractor class
"""
import re
import math

class tweetFeatureExtractor:
	"""
	tweetFeatureExtractor Class
	"""
	
	def __init__(self, emotionDict, wnaDict = {}):
		"""
		Initializes the tweetFeatureExtractor Class
		Parameters:
			1. emotionDict: Dictionary that maps emotion to a number and vice versa. The numbers should be consecutive starting from 1.
			2. wnaDict (optional): This Dictonary maps words in Word net affect to its emotion. Key is emotion and value is a list of words.
		"""
		self.sw = ['\'', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'a', 'an', 'the', 'and', 'if', 'or', 'because', 'as', 'of', 'at', 'by', 'for', 'with', 'about', 'between', 'into', 'through', 'during', 'before', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
		self.emotionDict = emotionDict.copy()
		self.wnaDict = wnaDict.copy()
	
	def getUnigramDict(self, words, d = {}):
		"""
		This functions adds unigram features to a feature dictionary. Parameters:
			1. words: List of words in the tweet/sentence.
			2. d (optional): Existing dictionary d is populated with these features. If d is not provided a dictionary containg only unigram features is returned. If d is provided, these features are added to existed d and a copy of updated dictionary is returned.
			
		Words latter in the sentence are given higher weights
		
		return: Dictionary containing key as unigram feature and value as its weight
		rtyrpe: Dictionary			
		"""
		l = len(words)
		for i in range(len(words)):
			word = words[i]
			w = math.ceil(float(i)/l + 0.5)
			if word in self.sw:
				continue
			feature = 'u(%s)' %(word)
			
			if d.has_key(feature):
				d[feature] += w
			else:
				d[feature] = w
		return d
	
	def getWnaDict(self, words, d = {}):
		"""
		This functions adds features which correspond to count of words in sentence that match with labels in Word net affect corpus. These features are added to a dictionary. Parameters:
			1. words: List of words in the tweet/sentence.
			2. d (optional): Existing dictionary d is populated with these features. If d is not provided a dictionary containg only wna features is returned. If d is provided, these features are added to existed d and a copy of updated dictionary is returned.
			
		
		return: Dictionary containing key as unigram feature and value as its weight
		rtyrpe: Dictionary
		"""
		for label in self.wnaDict.keys():
			feature = "wna(%s)" %(label)
			count  = 0
			wordlist = self.wnaDict[label]
			for word in words:
				if word in wordlist:
					count += 1
			value = count
			d[feature] = value
		return d
	
	def getDictString(self, d):
		"""
		This function converts the dictionary containing features to a string. The string returned is consistent with the MEGA Model Optimization Package expectations. Parameters:
			1. d: Dictionary where keys are features and corresponding values are weights for the feature.
		
		return: Feature String consistent with the MEGAM package
		rtype: String
		"""
		s = ""
		for (key, value) in d.items():
			s1 = "%s %d" %(key, value)
			s = s + s1 + " "
		return s
	
	def corpusExtract(self, corpusFile, outputFile):
		"""
		This function extracts features from a corpus containing tweets and outputs the features in file. The features that are saved in the file are consistent with MEGAM package used for training. Parameters:
			1. corpusFile: File name of the corpus. It should be a text file with each line having the following format: "tweet_id,Annotated emotion,tweet_text"
			2. outputFile: File name with the features will be saved. Format of this file "emotion_id feature_1 value_1 ... feature_n value_n"
		"""
		c = open(corpusFile, 'r')
		o = open(outputFile, 'w')
		line = c.readline()
		
		while line:
			fields = line.strip().split(',')
			emotion = fields[1].strip()
			emotion = self.emotionDict[emotion]
			tweet_text = " ".join(fields[2:])
			tweet_text = tweet_text.strip()
			d = self.tweetExtract(tweet_text)
			s = self.getDictString(d)
			l = "%d %s\n" %(emotion, s)
			o.write(l)
			line = c.readline()
		c.close()
		o.close()
			
	
	def batchExtract(self, tweetList):
		"""
		This function extracts features from a list of tweets. Parameters:
			1. tweetList: List of tweet texts.
		
		return: List of features for every tweet in tweetList
		rtype: list
		"""
		tweetFeatureList = []
		for i in range(len(tweetList)):
			d = self.tweetExtract(tweetList[i])
			tweetFeatureList.append(d)
		return tweetFeatureList
			
	def preprocess_tweet(self,tweet_text):
		"""
		This function preprocesses the tweet text. Handles hashtags, punctuations etc. Parameters:
			1. tweet_text: text of each tweet
		return: preprocessed tweet text
		rtype: string
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
	
	def tweetExtract(self, tweet_text):
		"""
		Extracts features from the given tweet text. Parameters:
			1. tweet_text: string of tweet text
		
		return: A feature dictionary where keys are features and corresponding value is weight for that feature
		rtype: dict
		"""
		d = dict()
		tweet_text = self.preprocess_tweet(tweet_text)
		tokens = tweet_text.split()
		self.getUnigramDict(tokens, d)
		self.getWnaDict(tokens, d)
		return d.copy()
