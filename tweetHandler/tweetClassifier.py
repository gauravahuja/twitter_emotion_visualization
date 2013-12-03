"""
Classifier Class
"""
import os
import math

class tweetClassifier:
	"""
	"""
	
	def __init__(self, emotionDict):
		"""
		"""
		self.emotionDict = emotionDict.copy()
	
	def train(self, trainCorpusFile, outputFile, megamPath = ""):
		"""
		"""
		if (megamPath == "" and os.getenv('MEGAMPATH') == None):
			print "megam path not set"
			return 0
		if(megamPath == ""):
			megamPath = os.getenv('MEGAMPATH')
		
		cmd = "%s/megam -fvals multiclass %s > %s" %(megamPath, trainCorpusFile, outputFile)
		print cmd
		s = os.system(cmd)	
		
	
	def load(self, weightFile):
		"""
		"""
		f = open(weightFile)
		self.featureDict = {}
		
		line = f.readline()
		while line:
			fields = line.strip().split()
			feature = fields[0].strip()
			weights = [float(x) for x in fields[1:]]
			self.featureDict[feature] = [0]*len(weights)
			for i in range(len(weights)):
				self.featureDict[feature][i] = weights[i]
			line = f.readline()
			
		f.close()
		
	
	def tweetClassify(self, feature_dict, threshold = 0.5):
		"""
		"""
		scores = [0]*8
		for i in range(8):
			s = self.featureDict['**BIAS**'][i]
			for (feature, value) in feature_dict.items():
				s += self.featureDict.get(feature, [0.0]*8)[i]*value
			scores[i] = s
		scores1 = [math.exp(x) for x in scores]
		s = sum(scores1)
		scores = [x/s for x in scores1]
		m = max(scores)
		if (m >= threshold):
			emotionI = scores.index(m)
			emotion = self.emotionDict[emotionI]
		else:
			emotionI = 0
			emotion = "neutral"
		return (emotionI, emotion)
	
	def corpusClassify(self, testFile):
		"""
		"""
		f = open(testFile)
		tweets = f.readlines()
		f.close()
		count = len(tweets)
		correct = 0
		emotionMatrix={}
		for i in range(8):
			emotionMatrix[i] = [0]*3

		for tweet in tweets:
			fields = tweet.strip().split()
			emotion = int(fields[0].strip())
			features_list = fields[1:]
			features_dict = {}
			for i in range(0, len(features_list), 2):
				feature = features_list[i].strip()
				value = float(features_list[i+1].strip())
				features_dict[feature] = value
			
			emotionMatrix[emotion][2] += 1
			(pEmotion, pEmotionName) = self.tweetClassify(features_dict)
			emotionMatrix[pEmotion][1] += 1
			if pEmotion == emotion:
				correct+=1
				emotionMatrix[emotion][0] += 1
		stats = {}
		print "Emotion\t\tPrecision\tRecall\tF-measure"
		for i in range(1, 8):
			emotionN = self.emotionDict[i]
			stats[emotionN] = [0]*3
			p = float(emotionMatrix[i][0]+1)/float(emotionMatrix[i][1]+1)
			r = float(emotionMatrix[i][0]+1)/float(emotionMatrix[i][2]+1)
			f = 2*p*r/(p+r)
			stats[emotionN][0]  = p
			stats[emotionN][1]  = r
			stats[emotionN][2]  = f
			print "%s\t\t%.2f\t\t%.2f\t\t%.2f" %(emotionN, p, r, f)
		return stats
