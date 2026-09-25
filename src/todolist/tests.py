from django.test import TestCase
from .models import List, Item

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        my_list = List()
        my_list.save()

        first_item = Item(text='I am the first item.')
        first_item.list = my_list
        first_item.save()

        second_item = Item(text='I am the second item.')
        second_item.list = my_list
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, my_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, 'I am the first item.')
        self.assertEqual(saved_items[0].list, my_list)
        self.assertEqual(saved_items[1].text, 'I am the second item.')
        self.assertEqual(saved_items[1].list, my_list)


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'home.html')

    def test_renders_homepage_content(self):
        response = self.client.get('/todo/')
        self.assertContains(response, 'To-Do')

    def test_renders_input_form(self):
        response = self.client.get("/todo/")
        self.assertContains(response, '<form action="/todo/lists/new/" method="post">')
        self.assertContains(response, 'name="item_text"')


class ListViewTest(TestCase):
    def test_renders_input_form(self):
        response = self.client.get("/todo/lists/the-ultimate-list/")
        self.assertContains(response, '<form action="/todo/lists/new/" method="post">')
        self.assertContains(response, 'name="item_text"')

    def test_display_all_list_items(self):
        # Arrange/Given
        the_list = List.objects.create()
        Item.objects.create(text='foo', list=the_list)
        Item.objects.create(text='bar', list=the_list)

        # Act/When
        response = self.client.get('/todo/lists/the-ultimate-list/')

        # Assert/Then
        self.assertContains(response, 'foo')
        self.assertContains(response, 'bar')

    def test_uses_list_view_template(self):
        response = self.client.get('/todo/lists/the-ultimate-list/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
    def test_can_save_post_request(self):
        self.client.post('/todo/lists/new/', {'item_text': 'A new item.'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.last().text, 'A new item.')

    def test_redirect_after_post_request(self):
        response = self.client.post('/todo/lists/new/', {'item_text': 'A new item.'})
        self.assertRedirects(response, '/todo/lists/the-ultimate-list/')
