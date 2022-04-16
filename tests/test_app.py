import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask import url_for, request, template_rendered
from app import create_app, db, Record
from dataprep import API_URL, download_articles, prepare_articles, new_data_into_ml_features
from config import api_key
import pytest
import pickle


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test_site.db'
         }
    )
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **kwargs):
        recorded.append((template, context))

    template_rendered.connect(record, app)

    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestHomePage:

    def test_root_url_resolves_to_home_page_view(self, app):
        with app.test_request_context():
            self.url = url_for('index')
        assert self.url == '/'

    def test_home_page_returns_correct_html(self, app, captured_templates):
        with app.test_client() as test_client:
            response = test_client.get('/')
            assert response.data.startswith(b'<!DOCTYPE html>')
            assert b'<title>AptNoise</title>' in response.data
            assert response.data.endswith(b'</html>\n')

            assert len(captured_templates) == 1

            template, context = captured_templates[0]

            assert template.name == "index.html"


class TestRecordModel:
    def test_new_record(self):
        record = Record(source_name='The Guardian', predicted_score_when_presented=50)
        assert record.source_name == 'The Guardian'
        assert record.predicted_score_when_presented == 50

    def test_saving_records(self, app):
        article_content = '''
            In the last week a curious video has been gaining popularity like a snowball. Mr Fluffy Ears owned 
            by the Smiths family turned out to be a magnificent singer showing off his skills in one of Mozart's
            classics. His performance of Cherubino's aria from the 18th century opera The Marriage of Figaro has won 
            the hearts of hundreds of thousands music-lovers. 
            According to the Smiths, Mr Fluffy Ears had a passion for music since he was a puppy...[+5433 chars]
            '''

        record = Record(
            author='John Doe',
            title="Dog Sings The Entire Cherubino's Aria",
            url='http://www.best-doggo-news.com',
            published_at='2022-02-20T15:42:54',
            content=article_content,
            source_name='Doggo News',
            predicted_score_when_presented=50,
            assigned_score=98,
            is_test_record=0
        )

        with app.test_request_context():
            db.session.add(record)
            db.session.commit()

            saved_record = Record.query.first()
        assert saved_record == record


class TestMLModel:
    def test_input_data(self):
        raw_articles = download_articles(API_URL, api_key)
        input_data = prepare_articles(raw_articles)
        assert len(input_data) > 0
        assert input_data.columns.to_list() == ['author', 'title', 'url', 'content', 'source_name']

    def test_ml_model(self):
        data_into_model = new_data_into_ml_features()
        ml_model = pickle.load(open('ml_model.pkl', 'rb'))
        predictions = ml_model.predict(data_into_model)
        assert predictions.any()

