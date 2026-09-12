from django.http import HttpRequest
from django.test import TestCase

from .models import Item
from .views import home_page


# Create your tests here.
class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'home.html')

    def test_renders_homepage_content(self):
        response = self.client.get('/todo/')
        self.assertContains(response, 'To-Do')

    # todo: this test is long-winded.
    def test_can_save_post_request(self):
        response = self.client.post('/todo/', {'item_text': 'A new item.'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(pk=1).text, 'A new item.')
        self.assertContains(response, 'A new item.')
        self.assertTemplateUsed('home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)