import json
import os
import preproc, date_parser
from collections import Counter
import pandas as pd
import streamlit as st

SCRIPT_DIR = os.path.dirname(__file__)

def sentiment_verbs():
    with open(f'{SCRIPT_DIR}/sentiment/verbs.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def sentiment_nouns():
    with open(f'{SCRIPT_DIR}/sentiment/emo_clean.json', 'r', encoding='utf-8') as file:
        return json.load(file)

VERBS = sentiment_verbs()
NOUNS = sentiment_nouns()


def get_sentiment_from_verbs(lemmas):
    res = []
    matching = set(lemmas) & set(VERBS.keys())
    lemmas_dict = Counter(lemmas)
    if matching:
        for word in matching:
            for _, sentiment in VERBS[word]:
                s = [sentiment] * lemmas_dict[word]
                res.extend(s)
        return Counter(res)
    else: return Counter()
   
def get_sentiment_from_nouns(lemmas):
    res = []
    matching = set(lemmas) & set(NOUNS.keys())
    lemmas_dict = Counter(lemmas)
    if matching:
        for word in matching:
            for sentiment in NOUNS[word]:
                s = [sentiment] * lemmas_dict[word]
                res.extend(s)
        return Counter(res)
    else: return Counter()

def get_overall_sentiment(tokens):
    lemmas = preproc.get_all_lemmas(tokens)
    verbs = get_sentiment_from_verbs(lemmas)
    nouns = get_sentiment_from_nouns(lemmas)
    return verbs + nouns


def get_sentiment_index(sentiments):
  return sentiments['positive'] - sentiments['negative']


def get_most_sentiment(sentiment_index):
  sentiments = []
  for index in sentiment_index:
    if index > 0:
      sentiments.append('positive')
    elif index < 0:
      sentiments.append('negative')
    else:
      sentiments.append('neutral')
  sentiments = Counter(sentiments)
  return sentiments.most_common(1)[0][0]

@st.experimental_memo
def data_for_sentiment_chart(df):
    df = df.copy()
    df['n_date'] = df.apply(lambda row: 
                                date_parser.normalize_dates(row.date_start, row.date_stop),
                                axis=1)
    return df[['n_date', 'sent_index']]
