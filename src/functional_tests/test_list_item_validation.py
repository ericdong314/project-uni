from unittest import skip

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from todolist.forms import DUPLICATE_ITEM_ERROR
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.live_server_url + '/todo/')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request and does not load the list page.
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid"))

        # She starts typing some characters in and the error disappears
        self.get_item_input_box().send_keys("Purchase milk")
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid"))

        # And she can submit successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Purchase milk")

        # Perversely, she now decides to submit a second blank list item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # which is similarly fend off by the browser
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:invalid"))

        # And she can correct it by filling some text in
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(lambda: self.browser.find_element(By.CSS_SELECTOR, "#id_text:valid"))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("2: Make tea")

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.live_server_url + '/todo/')
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy wellies")

        # She accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element(By.CSS_SELECTOR, ".invalid-feedback").text,
                DUPLICATE_ITEM_ERROR,
            )
        )
