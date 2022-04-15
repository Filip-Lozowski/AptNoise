import pickle
import re

import numpy as np
import requests
import pandas as pd
import sqlite3

from config import api_url, api_key

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


def prepare_articles(articles):
    df_for_ml = pd.json_normalize(articles.json()['articles'])
    renaming_dict = {
        'publishedAt': 'published_at',
        'source.name': 'source_name'
    }
    df_for_ml.rename(columns=renaming_dict, inplace=True)
    df_for_ml = df_for_ml[['author', 'title', 'url', 'content', 'source_name']]

    return df_for_ml


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
    articles.dropna(subset='content', inplace=True)
    articles['content_length_chars'] = articles.apply(derive_content_length, axis=1)
    articles.dropna(subset='content_length_chars', inplace=True)

    cols = FEATURE_COLS + ['assigned_score']
    articles = articles[cols].copy()

    return articles


def new_data_into_ml_features():
    raw_articles = download_articles(api_url, api_key)
    articles_df = prepare_articles(raw_articles)

    articles_df.dropna(subset='content', inplace=True)
    articles_df['content_length_chars'] = articles_df.apply(derive_content_length, axis=1)
    articles_df.dropna(subset='content_length_chars', inplace=True)
    articles_df.drop(columns='content', inplace=True)

    articles_df = articles_df[FEATURE_COLS]
    encoder = pickle.load(open('source_encoder.pkl', 'rb'))
    articles_df[CAT_COLS] = encoder.transform(articles_df[CAT_COLS])

    return articles_df
