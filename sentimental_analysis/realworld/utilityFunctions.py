import re
import string
from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

linkPattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


def removeLinks(text):
    return re.sub(linkPattern, '', text)

def stripEmojis(text):
    return text.encode('ascii', 'ignore').decode('ascii')


def stripPunctuations(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def stripExtraWhiteSpaces(text):
    return text.strip()

def removeSpecialChar(text):
    return re.sub(r'\W+ ', '', text)


def sentiment_scores(sentence):
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    return sentiment_dict
