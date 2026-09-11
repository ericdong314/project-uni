from django.http import HttpRequest
from django.test import TestCase
from .views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'home.html')

    def test_renders_homepage_content(self):
        response = self.client.get('/todo/')
        self.assertContains(response, 'To-Do')

    def test_add_item(self):
        response = self.client.post('/todo/', {'item_text': 'A new item.'})
        self.assertContains(response, 'A new item.')
