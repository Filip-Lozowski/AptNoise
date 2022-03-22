import re

import numpy as np
import requests
import pandas as pd
import sqlite3


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


def db_to_df():
    con = sqlite3.connect('site.db')
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
