"""
@package Corpus Handler

Provides the follwing classes:
	1. tweetDownloader: Assits in downloaded tweets from given tweet ids.
	2. tweetPreprocessor: Preprocess the tweets downloaded using the tweetDownloader class
	3. wnaParser: Parses the Word net affect corpus.
"""

from tweetDownloader import *
from tweetPreprocessor import *
from wnaParser import *

import logging

logger = logging.getLogger("corpusHandler")
logger.setLevel(logging.INFO)

handler = logging.FileHandler('corpusHandler.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

