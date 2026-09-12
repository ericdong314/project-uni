import time
import unittest

from django.test import LiveServerTestCase, override_settings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def assert_text_in_table(self, text):
        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(text, [row.text for row in rows])

    # @override_settings(DEBUG=True)  # <-- This forces Django to show the actual error page/traceback
    def test_create_items(self):
        # Alison visits the website and notices that the page title and header mention to-do lists.
        self.browser.get(self.live_server_url + '/todo/')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to create a to-do item with a text box straight away.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # She types in it "Buy a new pen."
        input_box.send_keys('Buy a new pen.')

        # She then presses enter and the page updates and shows
        # "1: Buy a new pen." as an item in a to-do list.
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assert_text_in_table('1: Buy a new pen.')

        # There is still an input box inviting he to add another item.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # She now enters "Buy a notebook." in the input box.
        # She presses enter and the page updates with both items displayed on the list.
        input_box.send_keys("Buy a notebook.")
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        self.assert_text_in_table('1: Buy a new pen.')
        self.assert_text_in_table('2: Buy a notebook.')

        # She is now happy and closes the tab.
