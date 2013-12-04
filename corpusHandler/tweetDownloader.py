"""
Tweet Downloader
"""

import tweepy
import time
import sys
from select import select
from collections import deque
import json
import logging


class tweetDownloader:
	"""
	Tweet Downloader class
	"""
	maxTweetsInWindow = 180 #Number of tweets that can be downloaded in the given time window
	tweetWindow = 15*60	#Time window in seconds
	statusFileSuffix = "_status"
	tweetStatus = {"completed":1, 1:"completed", "notCompleted":2, 2:"notCompleted" , "error88":3, 3:"error88", "error":4, 4:"error"}
	
	def __init__(self, consumer_key, consumer_secret, access_key, access_token_secret, download_dir, tweetList_file):
		"""
		Initializes the tweetDownloader instance with
			consumer_key: Twitter application consumer key
			consumer_secret: Twitter application consumer secret
			access_key: Access key of Twitter user who has authorized this app
			access_token_secret: Access token secret of Twitter user who has authorized this app
			download_dir: Directory where the tweets will be directed
			tweetList_file: File where each line specifies a tweet id
		"""
		self.logger = logging.getLogger("corpusHandler.tweetDownloader.%s" %(tweetList_file))
		self.logger.setLevel(logging.DEBUG)
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_key = access_key
		self.access_token_secret = access_token_secret
		self.download_dir = download_dir
		self.tweetList_file = tweetList_file
		self.tweetStatus_file = tweetList_file+tweetDownloader.statusFileSuffix
		self.notCompleted = {}
		self.completed = {}
		self.error88 = {}
		self.error = {}
		self.q = deque()
		try:
			self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
			self.auth.set_access_token(self.access_key, self.access_token_secret)
			self.api = tweepy.API(self.auth, parser=tweepy.parsers.RawParser())
		except:
			self.logger.critical("Twitter authentication failed. Exiting...")
			sys.exit(0)
		self.initialize()
		self.logger.info("Initialized tweetDownloader")
		
	def initialize(self):
		"""
		Internal Function. Used Internally	
		"""
		for i in range(tweetDownloader.maxTweetsInWindow):
			self.q.append(time.time())
		try:
			f = open(self.tweetStatus_file, 'r')
			lines = f.readlines()
			f.close()
		except:
			lines = []
	
		if(len(lines) == 0):
			f = open(self.tweetList_file, 'r')
			lines = f.readlines()
			f.close()
			for i in range(len(lines)):
				tid = lines[i].strip().split()[0]
				tid = int(tid)
				self.notCompleted[tid] = tweetDownloader.tweetStatus["notCompleted"]
		else:
			for i in range(len(lines)):
				(tid, status) = lines[i].strip().split()
				tid = int(tid)
				if status == "completed":
					self.completed[tid] = tweetDownloader.tweetStatus["completed"]
				elif status == "notCompleted":
					self.notCompleted[tid] = tweetDownloader.tweetStatus["notCompleted"]
				elif status == "error88":		
					self.error88[tid] = tweetDownloader.tweetStatus["error88"]
				else:
					self.error[tid] = tweetDownloader.tweetStatus["error"]
		
	def saveStatus(self):
		"""
		Internal function. Used Internally
		"""
		lines = []
		nc = 0
		for (tid, status) in self.notCompleted.items():
			nc = nc+1
			line = "%d %s\n" %(tid, tweetDownloader.tweetStatus[status])
			lines.append(line)
		e88 = 0
		for (tid, status) in self.error88.items():
			e88 = e88 +1
			line = "%d %s\n" %(tid, tweetDownloader.tweetStatus[status])
			lines.append(line)
		e = 0
		for (tid, status) in self.error.items():
			e = e+1
			line = "%d %s\n" %(tid, tweetDownloader.tweetStatus[status])
			lines.append(line)
		c = 0
		for (tid, status) in self.completed.items():
			c = c +1
			line = "%d %s\n" %(tid, tweetDownloader.tweetStatus[status])
			lines.append(line)
		
		lines[-1] = lines[-1].strip()
		f = open(self.tweetStatus_file, 'w')
		f.writelines(lines)
		f.close()
		self.logger.info("Downloaded %d, Error %d, Remaining %d" %(c, e+e88, nc))
		
	def getTweetFile(self,tid):
		"""
		Internal Function used internally
		"""
		fileName = "%s/%d.json" %(self.download_dir,tid)
		return fileName
		
	def downloadTweet(self, tid):
		"""
		Internal Function used internally
		"""
		del self.notCompleted[tid]
		status = -1
		try:
			s = self.api.get_status(id = tid)
			f = open(self.getTweetFile(tid), 'w')
			f.write(s)
			f.close()
			self.completed[tid] = tweetDownloader.tweetStatus["completed"]
			status = self.completed[tid]
		except tweepy.TweepError as e:
			try:
				e = json.loads(str(e))
				ecode = e["errors"][0]["code"]
			except:
				ecode = -1
			if ecode == 88:
				self.error88[tid] = tweetDownloader.tweetStatus["error88"]
				status = self.error88[tid]
			else:
				self.error[tid] = tweetDownloader.tweetStatus["error"]
				status = self.error[tid]
		self.logger.debug("Downloading tweet: %d, Status: %s" %(tid, tweetDownloader.tweetStatus[status]))

	def download(self):
		"""
		After initialization this function should be called to start the downloading process.
		"""
		tids = self.notCompleted.keys()
		inccount = len(tids)
		TI = 0
		windowCount = 0
		while (TI != inccount):
			t = self.q.popleft()
			tid = tids[TI]
			TI = TI+1
		
			sleepTime = t - time.time()
			sleepTime = int(sleepTime)+1
			if sleepTime <= 0:
				self.downloadTweet(tid)
			else:
				time.sleep(sleepTime)
				self.downloadTweet(tid)
			self.q.append(time.time()+tweetDownloader.tweetWindow)
		
			windowCount = windowCount + 1
		
			if (windowCount == tweetDownloader.maxTweetsInWindow):
				windowCount = 0
				self.saveStatus()
			
		self.saveStatus()			
