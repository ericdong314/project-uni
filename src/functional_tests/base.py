import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    host = '0.0.0.0'
    port = 8001

    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Remote('http://host.docker.internal:4444', options=options)
        if test_server := os.environ.get('TEST_SERVER'):
            self.live_server_url = 'http://' + test_server
        else:
            self.live_server_url = f'http://localhost:{self.port}'

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_list_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                self.assertIn(text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() > start_time + MAX_WAIT:
                    raise
                time.sleep(0.5)

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)
