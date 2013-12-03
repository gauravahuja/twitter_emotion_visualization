"""
Tweet Feature extractor class
"""
import re
import math

class tweetFeatureExtractor:
	"""
	"""
	
	def __init__(self, emotionDict, wnaDict = {}):
		"""
		"""
		self.sw = ['\'', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'a', 'an', 'the', 'and', 'if', 'or', 'because', 'as', 'of', 'at', 'by', 'for', 'with', 'about', 'between', 'into', 'through', 'during', 'before', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
		self.emotionDict = emotionDict.copy()
		self.wnaDict = wnaDict.copy()
	
	def getUnigramDict(self, words, d = {}):
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
		s = ""
		for (key, value) in d.items():
			s1 = "%s %d" %(key, value)
			s = s + s1 + " "
		return s
	
	def corpusExtract(self, corpusFile, outputFile):
		"""
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
		"""
		tweetFeatureList = []
		for i in range(len(tweetList)):
			d = self.tweetExtract(tweetList[i])
			tweetFeatureList.append(d)
		return tweetFeatureList
			
	def preprocess_tweet(self,tweet_text):
		"""
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
		"""
		d = dict()
		tweet_text = self.preprocess_tweet(tweet_text)
		tokens = tweet_text.split()
		self.getUnigramDict(tokens, d)
		self.getWnaDict(tokens, d)
		return d.copy()
