import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import api_key
from dataprep import download_articles, db_to_df


def test_download_articles_response_ok():
    api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    response = download_articles(api_url, api_key)

    assert response.status_code == 200


def test_download_articles_is_json():
    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    response = download_articles(api_url, api_key)

    assert isinstance(response.json(), dict)


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
