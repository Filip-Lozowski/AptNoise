import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from flask import url_for, request, template_rendered
from app import create_app
import pytest

app = create_app()


@pytest.fixture
def captured_templates():
    recorded = []

    def record(sender, template, context, **kwargs):
        recorded.append((template, context))

    template_rendered.connect(record, app)

    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


class TestHomePage:

    def test_root_url_resolves_to_home_page_view(self):
        with app.test_request_context():
            self.url = url_for('index')
        assert self.url == '/'

    def test_home_page_returns_correct_html(self, captured_templates):
        with app.test_client() as test_client:
            response = test_client.get('/')
            assert response.data.startswith(b'<!DOCTYPE html>')
            assert b'<title>AptNoise</title>' in response.data
            assert response.data.endswith(b'</html>\n')

            assert len(captured_templates) == 1

            template, context = captured_templates[0]

            assert template.name == "index.html"
