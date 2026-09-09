from django.db.models import Model
from django.http.request import HttpRequest
from django.test import TestCase
from django.urls import resolve

from .views import home_page
from .models import Item


# Create your tests here.

class TestHomePage(TestCase):
    def test_url_mapped_to_the_view(self):
        match = resolve('/klipper/')
        self.assertEqual(match.func, home_page)

    def test_view_uses_correct_template(self):
        response = self.client.get('/klipper/')
        self.assertTemplateUsed(response, 'home.html')

    def test_view_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Klipper</title>', html)


class TestAddItem(TestCase):
    example_link = 'https://example.com/'

    def test_add_item(self):
        self.client.post('/klipper/create/', data={'link': self.example_link})
        item = Item.objects.last()
        self.assertEqual(item.link, self.example_link)

    def test_list_items(self):
        Item.objects.create(link=self.example_link)
        response = self.client.get('/klipper/')
        self.assertContains(response, self.example_link)
