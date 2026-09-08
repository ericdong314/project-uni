import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        ...

    def tearDown(self) -> None:
        self.browser.quit()

    def test_create_items(self):
        # Alison visits the website and notices that it is a to-do list app.
        self.browser.get('http://localhost:8000/todo/')
        self.assertIn('To-Do', self.browser.title)

        # She is invited to create a to-do item straight away.
        # She sees an input box and types in it "Buy a new pen."
        self.fail('Manual fail')

        # She then presses enter and the page updates and shows
        # "1. Buy a new pen." as an item in a to-do list.

        # She now enters "Buy a notebook." in the input box.

        # She presses enter and the page updates with both items displayed on the list.

        # She is now happy and closes the tab.


if __name__ == '__main__':
    unittest.main()
