from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from dataprep import download_articles
from config import api_key

api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='
response = download_articles(api_url, api_key)
articles_list = response.json()['articles']
links_list = []
for article in articles_list:
    links_list.append(article['url'])


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        return render_template('index.html', links_list=links_list)

    return app
