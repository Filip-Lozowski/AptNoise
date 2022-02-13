from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class TestUsersPerspective:
    @classmethod
    def setup_class(cls):
        cls.browser = webdriver.Firefox()

    @classmethod
    def teardown_class(cls):
        cls.browser.quit()

    def test_read_rate_and_reload(self):
        # open the app
        self.browser.get('http://localhost:5000')

        # check if this is a news app that is called Apt Noise
        assert "AptNoise" in self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        assert "Apt Noise" in header_text

        # Notice some article titles displayed in a table
        table = self.browser.find_element(By.ID, 'id_articles_table')
        assert table

        # Click at the first article title to read it on its original page
        link = self.browser.find_element(By.TAG_NAME, 'a')
        assert link

        # assign a score to the article by typing it into a box near the link
        input_box = self.browser.find_element(By.ID, 'id_score')
        assert input_box
        input_box.send_keys('57')

        # Save the scores by clicking on a button
        save_scores = self.browser.find_element(By.ID, 'id_save_score')
        assert save_scores
        save_scores.click()

        # The app reloads
        time.sleep(3)

        # Previously rated article disappeared
        reload_link = self.browser.find_element(By.TAG_NAME, 'a')
        assert link != reload_link
