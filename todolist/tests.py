from django.http import HttpRequest
from django.test import TestCase
from .views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>To-Do lists<title/>', html)
        self.assertStartsWith(html, '<html>')
        self.assertEndsWith(html, '<html/>')
