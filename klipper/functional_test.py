from selenium import webdriver
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

        # Eric enters the link to his favourite website and presses enter.

        # The page updates with the link added to the page as an item in a list.
        self.fail('To complete')


if __name__ == '__main__':
    unittest.main()
