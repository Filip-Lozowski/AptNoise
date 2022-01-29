from flask import url_for
from app import app


class TestHomePage:

    def test_root_url_resolves_to_home_page_view(self):
        with app.test_request_context():
            self.url = url_for('index')
        assert self.url == '/'
