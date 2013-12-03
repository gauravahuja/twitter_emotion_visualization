"""
@package Corpus Handler
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

