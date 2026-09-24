from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from .models import Item
from .views import home_page


# Create your tests here.
class HomePageTest(TestCase):
    def test_renders_homepage_content(self):
        response = self.client.get('/todo/')
        self.assertContains(response, 'To-Do')

    def test_renders_input_form(self):
        response = self.client.get("/todo/")
        self.assertContains(response, '<form action="/todo/" method="post">')
        self.assertContains(response, 'name="item_text"')

    def test_can_save_post_request(self):
        self.client.post('/todo/', {'item_text': 'A new item.'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get(pk=1).text, 'A new item.')

    def test_redirect_after_post_request(self):
        response = self.client.post('/todo/', {'item_text': 'A new item.'})
        self.assertRedirects(response, '/todo/lists/the-ultimate-list/')

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
    def test_renders_input_form(self):
        response = self.client.get("/todo/lists/the-ultimate-list/")
        self.assertContains(response, '<form action="/todo/" method="post">')
        self.assertContains(response, 'name="item_text"')

    def test_display_all_list_items(self):
        # Arrange/Given
        Item.objects.create(text='foo')
        Item.objects.create(text='bar')

        # Act/When
        response = self.client.get('/todo/lists/the-ultimate-list/')

        # Assert/Then
        self.assertContains(response, 'foo')
        self.assertContains(response, 'bar')

    def test_uses_list_view_template(self):
        response = self.client.get('/todo/lists/the-ultimate-list/')
        self.assertTemplateUsed(response, 'list.html')

