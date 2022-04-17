from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from dataprep import get_new_articles_df, prepare_new_articles, create_features, CAT_COLS
import pandas as pd
import pickle
from random import randint


articles_df = get_new_articles_df()
data_into_model = prepare_new_articles(articles_df)
data_into_model = create_features(data_into_model)

encoder = pickle.load(open('cat_cols_encoder.pkl', 'rb'))
data_into_model[CAT_COLS] = encoder.transform(data_into_model[CAT_COLS])

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
        return f'''
        Record(
        id={self.id}, 
        author={self.author},
        title={self.title},
        url={self.url},
        published_at={self.published_at},
        content={self.content},
        source_name={self.source_name},
        predicted_score_when_presented={self.predicted_score_when_presented}, 
        assigned_score={self.assigned_score},
        is_test_record={self.is_test_record}
        )'''


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
