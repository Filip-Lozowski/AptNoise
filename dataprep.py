import requests
import pandas as pd


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
