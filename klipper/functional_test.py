import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest


class TestKlipper(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_user_add_website(self):
        # Eric opens the page 'klipper/' sees the title 'Klipper',
        self.browser.get('http://localhost:8000/klipper/')
        self.assertIn('Klipper', self.browser.title)

        # On the page, an input box invites him to enter a URL.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a URL')

        # Eric enters the link to his favourite website and presses enter.
        url = 'https://www.obeythetestinggoat.com/pages/book.html'
        input_box.send_keys(url)
        input_box.send_keys(Keys.ENTER)

        # The page updates with the link added to the page as an item in a list.
        time.sleep(1)
        table = self.browser.find_element(By.ID, 'id_items_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(any(url in row.text for row in rows), 'url not found in table')

        # There is still a text box inviting him to enter another URL.
        self.fail('To complete')


if __name__ == '__main__':
    unittest.main()
