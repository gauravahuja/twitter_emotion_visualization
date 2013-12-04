"""
@package Classifier and Feature extaction

This package includes the following classes:
	1. tweetFeatureExtractor
	2. tweetClassifier
	
tweetFeatureExtractor
This class extracts features form tweets. 
The features are unigrams and the presences of words from the emotional categories of Wordnet Affect.

tweetClassifier
This class uses Maximum entropy model to perform classification. 
In order to train the classifier requires Mega Model Optimization Package installed on the system.
This package can be downloaded from http://www.umiacs.umd.edu/~hal/megam/
"""

from tweetFeatureExtractor import *
from tweetClassifier import *
