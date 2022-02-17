from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from dataprep import download_articles
from config import api_key

api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='
response = download_articles(api_url, api_key)
articles_list = response.json()['articles']
links_list = []
for article in articles_list:
    links_list.append(article['url'])

db = SQLAlchemy()


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(40))
    score = db.Column(db.Integer)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html', link=links_list[0])
        if request.method == 'POST':
            score = request.form['item_score']
            del links_list[0]
            return redirect(url_for("index"))
    return app
