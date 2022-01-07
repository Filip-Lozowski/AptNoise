def test_download_articles_is_json():
    import sys
    import os

    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    # sys.path.append(r'./maindir')

    import requests
    from config import api_key

    api_url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(api_url)

    assert isinstance(response.json(), dict)
