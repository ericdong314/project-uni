import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 5


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        if test_server := os.environ.get('TEST_SERVER'):
            self.live_server_url = 'http://' + test_server

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

    def test_create_items(self):
        # Edith visits the website and notices that the page title and header mention to-do lists.
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

        self.wait_for_row_in_list_table('1: Buy a new pen.')

        # There is still an input box inviting he to add another item.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # She now enters "Buy a notebook." in the input box.
        # She presses enter and the page updates with both items displayed on the list.
        input_box.send_keys("Buy a notebook.")
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('2: Buy a notebook.')
        self.wait_for_row_in_list_table('1: Buy a new pen.')

        # She is now happy and closes the tab.

    def test_layout_and_styling(self):
        # Edith goes to the home page,
        self.browser.get(self.live_server_url + '/todo/')

        # Her browser window is set to a very specific size
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )
        # She starts a new list and sees the input is nicely
        # centered there too
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: testing")
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10,
        )

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith visits the site first and add an item to her list
        self.browser.get(self.live_server_url + '/todo/')
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy a new pen.')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy a new pen.')

        # Assert that Edith gets a url for her list
        url_edith = self.browser.current_url
        self.assertRegex(url_edith, '/todo/lists/.+')

        # Patrick now visits the site and add an item to his list.
        ## We use cookie deletion to simulate the change of users.
        self.browser.delete_all_cookies()
        self.browser.get(self.live_server_url + '/todo/')

        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('Buy a new pen.', page_text)
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        input_box.send_keys('Buy a watermelon.')
        input_box.send_keys(Keys.ENTER)

        # His item appears in the list
        self.wait_for_row_in_list_table('1: Buy a watermelon.')

        # Check that Patrick gets his own url.
        url_patrick = self.browser.current_url
        self.assertRegex(url_patrick, '/todo/lists/.+')
        self.assertNotEqual(url_patrick, url_edith)

        # Check that only Patrick's items are shown on his page.
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('Buy a watermelon.', page_text)
        self.assertNotIn('Buy a new pen.', page_text)
