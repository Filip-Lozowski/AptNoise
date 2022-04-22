import pickle
import re

import numpy as np
import requests
import pandas as pd
import sqlite3

from config import API_KEY
import __main__
from placeholder_model import PlaceholderEncoder, PlaceholderModel

__main__.PlaceholderEncoder = PlaceholderEncoder
__main__.PlaceholderModel = PlaceholderModel

API_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='

FEATURE_COLS = pickle.load(open('features.pkl', 'rb'))

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


def create_features(df, update_file=False, test=False):
    new_df = df.dropna(subset='content').copy()
    new_df['content_length_chars'] = new_df.apply(derive_content_length, axis=1)
    new_df.dropna(subset='content_length_chars', inplace=True)

    non_feature_cols = [
        'title',
        'url',
        'content',
    ]

    optional_non_features = [
        'published_at',
        'predicted_score_when_presented',
        'assigned_score',
        'is_test_record'
    ]

    actual_cols = new_df.columns.tolist()

    non_feature_cols = non_feature_cols + [col for col in optional_non_features if col in actual_cols]

    new_df.drop(columns=non_feature_cols, inplace=True)

    feature_cols = new_df.columns.tolist()

    if update_file:
        if test:
            suffix = '_test'
        else:
            suffix = ''

        pickle.dump(feature_cols, open(f'features{suffix}.pkl', 'wb'))

    return new_df


def db_into_ml(set_type, save_features=False):
    articles = db_to_df()

    if set_type == 'training':
        articles = articles[articles['is_test_record'] == 0]
    elif set_type == 'test':
        articles = articles[articles['is_test_record'] == 1]
    else:
        raise ValueError("Wrong set type specified.")

    articles = articles[articles['assigned_score'] != -999]
    articles = articles.drop_duplicates(subset=['title', 'published_at'])

    features = create_features(articles, update_file=save_features)
    df_into_ml = features.merge(articles[['assigned_score']], how='left', left_index=True, right_index=True)

    return df_into_ml


def new_data_into_ml_features(test=False):
    articles_df = get_new_articles_df()
    articles_df = prepare_new_articles(articles_df)
    articles_df = create_features(articles_df)

    if test:
        suffix = '_test'
    else:
        suffix = ''

    encoder = pickle.load(open(f'cat_cols_encoder{suffix}.pkl', 'rb'))
    articles_df[CAT_COLS] = encoder.transform(articles_df[CAT_COLS])

    return articles_df
