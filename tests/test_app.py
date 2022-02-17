import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask import url_for, request, template_rendered
from app import create_app, db, Record
import pytest


@pytest.fixture()
def app():
    app = create_app()
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

# Ten test jest chyba niepotrzebny
    def test_can_save_a_post_request(self, app, captured_templates):
        with app.test_client() as test_client:
            response = test_client.post('/', data={'item_score': '16'})
            assert '16' in response.data.decode()

            assert len(captured_templates) == 1

            template, context = captured_templates[0]
            assert template.name == "index.html"


class TestRecordModel:
    def test_saving_and_retrieving_records(self):
        first_record = Record(source='The Guardian', score=50)
        assert first_record.source == 'The Guardian'
        assert first_record.score == 50
