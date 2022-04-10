from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from dataprep import download_articles, new_data_into_ml_features
from config import api_key
import pandas as pd
import pickle
from random import randint

api_url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='

raw_articles = download_articles(api_url, api_key)
articles_df = pd.json_normalize(raw_articles.json()['articles'])

data_into_model = new_data_into_ml_features()
ml_model = pickle.load(open('ml_model.pkl', 'rb'))
predicted_scores = ml_model.predict(data_into_model)
predicted_scores = pd.Series(predicted_scores, name='predicted_score')

articles_df = pd.concat([articles_df, predicted_scores], axis=1)
articles_df.sort_values('predicted_score', inplace=True)


db = SQLAlchemy()


class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(40))
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    published_at = db.Column(db.String(30))
    content = db.Column(db.String(220))
    source_name = db.Column(db.String(40))
    predicted_score_when_presented = db.Column(db.Integer)
    assigned_score = db.Column(db.Integer)
    is_test_record = db.Column(db.Integer)

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
            rated_article = Record(
                author=articles_df.loc[articles_df.index[0], 'author'],
                title=articles_df.loc[articles_df.index[0], 'title'],
                url=articles_df.loc[articles_df.index[0], 'url'],
                published_at=articles_df.loc[articles_df.index[0], 'publishedAt'],
                content=articles_df.loc[articles_df.index[0], 'content'],
                source_name=articles_df.loc[articles_df.index[0], 'source.name'],
                predicted_score_when_presented=articles_df.loc[articles_df.index[0], 'predicted_score'],
                assigned_score=score,
                is_test_record=randint(0, 1)
            )
            db.session.add(rated_article)
            db.session.commit()
            articles_df.drop(index=articles_df.index[0], inplace=True)
            return redirect(url_for("index"))

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Record=Record)

    return app


if __name__ == '__main__':
    create_app()
