import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask import url_for, request, template_rendered
from app import create_app, db, Record
import pytest


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

# Ten test jest chyba niepotrzebny
#     def test_can_save_a_post_request(self, app, captured_templates):
#         with app.test_client() as test_client:
#             response = test_client.post('/', data={'item_score': '16'})
#             assert '16' in response.data.decode()
#
#             assert len(captured_templates) == 1
#
#             template, context = captured_templates[0]
#             assert template.name == "index.html"


class TestRecordModel:
    def test_new_record(self):
        record = Record(source='The Guardian', score=50)
        assert record.source == 'The Guardian'
        assert record.score == 50

    def test_saving_records(self, app):
        record = Record(source='The Guardian', score=50)
        with app.test_request_context():
            db.session.add(record)
            db.session.commit()

            saved_record = Record.query.first()
        assert saved_record == record





