from django.http.request import HttpRequest
from django.test import TestCase
from django.urls import resolve

from klipper.views import home_page


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
