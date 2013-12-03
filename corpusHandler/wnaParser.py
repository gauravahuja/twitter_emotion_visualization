"""
Word Net Affect Parser Class
"""
import cPickle as pickle
from nltk.stem.porter import PorterStemmer

class wnaParser:
	"""
	"""
	
	def __init__(self, wna_dir, wna_files):
		"""
		"""
		self.wna_dir = wna_dir
		self.wna_files = wna_files
	
	def parse(self, pickledFile):
		"""
		"""
		wnaEmotion_list = {}
		for fileName in self.wna_files:
			label = fileName.split('.')[0]
			fileName = self.wna_dir + '/' + fileName
			f = open(fileName)
			lines = f.readlines()
			f.close()
			wnaEmotion_list[label] = []
			for line in lines:
				words = line.strip().split()
				words = words[1:]
				wnaEmotion_list[label] += words
		f = open(pickledFile, 'wb')
		pickle.dump(wnaEmotion_list, f, protocol=2)
		f.close()
		return wnaEmotion_list.copy()
		
	def stemTokens(self, tokens):
		"""
		Stems each element in the tokens list using Porters algorithm
		:type tokens: list of unicode strings
		:param tokens: list of unicode strings in the document

		:return: list of stemmed words 
		:rtype: list
		"""

		stemmer = PorterStemmer()
		stemmedTokens = []
		for token in tokens:
		 stemmedTokens.append(stemmer.stem(token))
		return stemmedTokens
	
	def parse_stemmed(self, pickledFile):
		"""
		"""
		wnaEmotion_list = {}
		for fileName in self.wna_files:
			label = fileName.split('.')[0]
			fileName = self.wna_dir + '/' + fileName
			f = open(fileName)
			lines = f.readlines()
			f.close()
			wnaEmotion_list[label] = []
			for line in lines:
				words = line.strip().split()
				words = self.stemTokens(words[1:])
				wnaEmotion_list[label] += words
		f = open(pickledFile, 'wb')
		pickle.dump(wnaEmotion_list, f, protocol=2)
		f.close()
		return wnaEmotion_list.copy()
	
		

