import sys
import os

import numpy as np
import pandas as pd

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import api_key
from dataprep import download_articles, prepare_articles, db_to_df, derive_content_length



def test_download_articles_response_ok():
    api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    response = download_articles(api_url, api_key)

    assert response.status_code == 200


def test_download_articles_is_json():
    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    response = download_articles(api_url, api_key)

    assert isinstance(response.json(), dict)


def test_prepare_articles():
    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    articles = download_articles(api_url, api_key)
    df_result = prepare_articles(articles)
    expected_cols = ['author', 'title', 'url', 'content', 'source_name']

    assert df_result.columns.tolist() == expected_cols


def test_db_to_df():
    df = db_to_df()
    expected_cols = [
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

    assert df.columns.to_list() == expected_cols
    assert not df.empty
    assert not df.isnull().all().all()
    assert df.index.name == 'id'


def test_derive_content_length():
    content1 = '''
    In the last week a curious video has been gaining popularity like a snowball. Mr Fluffy Ears owned 
    by the Smiths family turned out to be a magnificent singer showing off his skills in one of Mozart's
    classics. His performance of Cherubino's aria from the 18th century opera The Marriage of Figaro has won 
    the hearts of hundreds of thousands music-lovers. 
    According to the Smiths, Mr Fluffy Ears had a passion for music since he was a puppy...[+5433 chars]
    '''
    content2 = ''
    content3 = 'This is a sample content without a number at the end.'

    df = pd.DataFrame(
        [
            ['John Doe', content1],
            ['Jane Doe', content2],
            ['', content3]
        ],
        columns=['author', 'content']
    )
    content_length = df.apply(derive_content_length, axis=1)

    assert content_length[0] == 5433
    assert np.isnan(content_length[1])
    assert np.isnan(content_length[2])


def test_db_into_ml():
    result_df = db_into_ml(set_type='training')
    expected_cols = ['author', 'source_name', 'content_length_chars', 'assigned_score']

    assert not result_df.isnull().all().all()
    assert not result_df.empty
    assert result_df.columns.to_list() == expected_cols


def test_new_data_into_ml_features():
    result_df = new_data_into_ml_features()
    expected_cols = ['author', 'source_name', 'content_length_chars']

    assert not result_df.isnull().all().all()
    assert not result_df.empty
    assert result_df.columns.to_list() == expected_cols
