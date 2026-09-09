import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        ...

    def tearDown(self) -> None:
        self.browser.quit()

    def test_create_items(self):
        # Alison visits the website and notices that the page title and header mention to-do lists.
        self.browser.get('http://localhost:8000/todo/')
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to create a to-do item with a text box straight away.
        input_box = self.browser.find_element(By.ID, 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        # She types in it "Buy a new pen."
        input_box.send_keys('Buy a new pen')

        # She then presses enter and the page updates and shows
        # "1: Buy a new pen." as an item in a to-do list.
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_list_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertTrue(any(row.text == '1: Buy a new pen.' for row in rows), 'New to-to item did not appear in table')

        # These is still an input box inviting he to add another item.
        # She now enters "Buy a notebook." in the input box.
        self.fail('Finish the test')

        # She presses enter and the page updates with both items displayed on the list.

        # She is now happy and closes the tab.


if __name__ == '__main__':
    unittest.main()
