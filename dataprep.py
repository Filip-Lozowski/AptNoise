import requests


def download_articles(api_url, key):
    articles_url = api_url + key
    response = requests.get(articles_url)

    return response


def transform_response_into_df():
    return None


def transform_raw_data():
    return None


def load_labeled_data():
    return None


def save_labeled_data():
    return None
