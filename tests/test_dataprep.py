import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from config import api_key
import dataprep as dp


def test_download_articles_response_ok():
    api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    response = dp.download_articles(api_url, api_key)

    assert response.status_code == 200


def test_download_articles_is_json():
    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey='
    response = dp.download_articles(api_url, api_key)

    assert isinstance(response.json(), dict)
