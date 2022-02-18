from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from dataprep import download_articles
from config import api_key
import pandas as pd

api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='
response = download_articles(api_url, api_key)
# articles_list = response.json()['articles']
articles_df = pd.json_normalize(response.json()['articles'])

db = SQLAlchemy()


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(40))
    score = db.Column(db.Integer)

    def __repr__(self):
        return f'Record(id={self.id}, source={self.source}, score={self.score})'


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            return render_template('index.html', link=articles_df.loc[articles_df.index[0], 'url'])
        if request.method == 'POST':
            score = request.form['item_score']
            rated_article = Record(source=articles_df.loc[articles_df.index[0], 'source.name'], score=score)
            db.session.add(rated_article)
            db.session.commit()
            articles_df.drop(index=articles_df.index[0], inplace=True)
            return redirect(url_for("index"))

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Record=Record)

    return app
