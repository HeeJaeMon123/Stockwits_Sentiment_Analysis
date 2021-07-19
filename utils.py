import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import json
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import datetime


nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')

LIKE_URL = "https://api.stocktwits.com/api/2/messages/like.json"
TRENDING_URL = "https://api.stocktwits.com/api/2/streams/trending.json"


def get_msg_with_tickers():
    res = requests.get(TRENDING_URL).json()

    j = json.dumps(res['messages'])
    info = json.loads(j)

    # df = pd.json_normalize(info)
    msg_tickers = {}
    for info in res['messages']:
        symbol_list = []
        for symbol in info['symbols']:
            symbol_list.append(symbol['symbol'])
        msg_tickers[info['body']] = symbol_list

    clean_msg_tickers = clean_tweets(msg_tickers)
    lemmatized_msg_tickers = lemmatize_tweet(clean_msg_tickers)

    return lemmatized_msg_tickers


def clean_tweets(msg_tickers):
    # http를 포함하는 링크 제거
    # msg_tickers = df.clean_tweet.map(lambda x: re.sub(r'http.*', '', x))
    clean_msg_tickers = {}
    stop_word_list = stopwords.words('english')
    for msg, ticker in msg_tickers.items():
        filtered_msg = re.sub(r'http.*', '', msg)
        filtered_msg = re.sub("\$[a-zA-Z]*", '', filtered_msg)
        # 특수 문자와 숫자 제거
        filtered_msg = re.sub(r"[^a-zA-Z]", ' ', filtered_msg)
        filtered_msg = filtered_msg.lower()

        tokens = word_tokenize(filtered_msg)

        # 토큰화를 진행 후 불용어 제거
        clean_tokens = [w for w in tokens if w not in stop_word_list]
        clean_msg_tickers[msg] = {'tokens': clean_tokens, 'tickers': ticker}
    return clean_msg_tickers


def lemmatize_tweet(msg_tickers):
    lemmatized_msg_tickers = {}
    lemmatizer = WordNetLemmatizer()

    for msg, info in msg_tickers.items():
        lem_words = []
        pos_tag_list = nltk.pos_tag(info['tokens'])
        wordnet_tags = convert_to_wordnet_compliant(pos_tag_list)

        for i in range(len(info['tokens'])):
            # Convert pos-tag to be wordnet compliant
            lem_words.append(lemmatizer.lemmatize(info['tokens'][i], pos=wordnet_tags[i]))
        lem_tweet = ' '.join(lem_words)
        lemmatized_msg_tickers[lem_tweet] = info['tickers']
    return lemmatized_msg_tickers


def convert_to_wordnet_compliant(pos_tag_list):
    wordnet_tags = []
    for j in pos_tag_list:
        if j[1].startswith('J'):
            # Adjective
            wordnet_tags.append(wordnet.ADJ)
        elif j[1].startswith('N'):
            # Noun
            wordnet_tags.append(wordnet.NOUN)
        elif j[1].startswith('R'):
            # Adverb
            wordnet_tags.append(wordnet.ADV)
        elif j[1].startswith('V'):
            # Verb
            wordnet_tags.append(wordnet.VERB)
        else:
            # Default to noun
            wordnet_tags.append(wordnet.NOUN)
    return wordnet_tags
