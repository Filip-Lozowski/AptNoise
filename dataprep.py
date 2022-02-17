import requests


def download_articles(api_url, key):
    articles_url = api_url + key
    response = requests.get(articles_url)

    return response
