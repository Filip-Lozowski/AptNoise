import pickle
import re

import numpy as np
import requests
import pandas as pd
import sqlite3

from config import API_KEY

API_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='

FEATURE_COLS = [
    'author',
    'source_name',
    'content_length_chars'
]

CAT_COLS = [
    'author',
    'source_name'
]


def download_articles(api_url, key):
    articles_url = api_url + key
    response = requests.get(articles_url)

    return response


def get_new_articles_df():
    articles_raw = download_articles(API_URL, API_KEY)
    articles_df = pd.json_normalize(articles_raw.json()['articles'])

    return articles_df


def prepare_new_articles(articles_df):
    renaming_dict = {
        'source.name': 'source_name'
    }
    articles_df = articles_df.rename(columns=renaming_dict).copy()
    articles_df = articles_df[['author', 'title', 'url', 'content', 'source_name']]

    return articles_df


def db_to_df(path='site.db'):
    con = sqlite3.connect(path)
    cur = con.cursor()

    cur.execute("SELECT * FROM record")
    articles = cur.fetchall()
    input_cols = [
        'id',
        'author',
        'title',
        'url',
        'published_at',
        'content',
        'source_name',
        'predicted_score_when_presented',
        'assigned_score',
        'is_test_record'
    ]
    articles_df = pd.DataFrame(articles, columns=input_cols)
    articles_df.set_index('id', inplace=True)

    return articles_df


def derive_content_length(row):
    content = row['content']

    if content:
        content_end = content[-20:]
        match = re.search(r'\d+', content_end)
    else:
        return None

    if match:
        content_length = match[0]
        return int(content_length)
    else:
        return np.nan


def create_features(df):
    new_df = df.dropna(subset='content').copy()
    new_df['content_length_chars'] = new_df.apply(derive_content_length, axis=1)
    new_df.dropna(subset='content_length_chars', inplace=True)
    new_df = new_df[FEATURE_COLS]

    return new_df


def db_into_ml(set_type):
    articles = db_to_df()

    if set_type == 'training':
        articles = articles[articles['is_test_record'] == 0]
    elif set_type == 'test':
        articles = articles[articles['is_test_record'] == 1]
    else:
        raise ValueError("Wrong set type specified.")

    articles = articles[articles['assigned_score'] != -999]
    articles = articles.drop_duplicates(subset=['title', 'published_at'])

    features = create_features(articles)
    df_into_ml = features.merge(articles[['assigned_score']], how='left', left_index=True, right_index=True)

    return df_into_ml


def new_data_into_ml_features():
    articles_df = get_new_articles_df()
    articles_df = prepare_new_articles(articles_df)
    articles_df = create_features(articles_df)

    encoder = pickle.load(open('source_encoder.pkl', 'rb'))
    articles_df[CAT_COLS] = encoder.transform(articles_df[CAT_COLS])

    return articles_df
