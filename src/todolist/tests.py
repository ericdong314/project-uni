from pkgutil import resolve_name

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
    def test_uses_list_view_template(self):
        my_list = List.objects.create()
        response = self.client.get(f'/todo/lists/{my_list.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/todo/lists/{mylist.id}/")
        self.assertContains(response, f'<form action="/todo/lists/{mylist.id}/add_item/" method="post">')
        self.assertContains(response, 'name="item_text"')

    def test_display_only_items_on_that_list(self):
        # Arrange/Given
        mylist = List.objects.create()
        Item.objects.create(text='foo', list=mylist)
        Item.objects.create(text='bar', list=mylist)

        another_list = List.objects.create()
        Item.objects.create(text='I should be on another_list', list=another_list)

        # Act/When
        response = self.client.get(f'/todo/lists/{mylist.id}/')

        # Assert/Then
        self.assertContains(response, 'foo')
        self.assertContains(response, 'bar')
        self.assertNotContains(response, 'I should be on another_list')


class NewListTest(TestCase):
    def test_can_save_post_request(self):
        self.client.post('/todo/lists/new/', {'item_text': 'A new item.'})
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.last().text, 'A new item.')

    def test_redirect_after_post_request(self):
        response = self.client.post('/todo/lists/new/', {'item_text': 'A new item.'})
        list_created = List.objects.get()
        self.assertRedirects(response, f'/todo/lists/{list_created.id}/')


class NewItemTest(TestCase):
    def test_can_save_post_request_to_an_existing_list(self):
        mylist = List.objects.create()
        self.client.post(f'/todo/lists/{mylist.id}/add_item/', {'item_text': 'first item.'})
        self.client.post(f'/todo/lists/{mylist.id}/add_item/', {'item_text': 'second item.'})
        self.assertEqual(Item.objects.filter(list=mylist).count(), 2)

    def test_redirect_after_post_request(self):
        mylist = List.objects.create()
        otherlist = List.objects.create()  # test for silliness
        response = self.client.post(f'/todo/lists/{mylist.id}/add_item/', {'item_text': 'A new item.'})
        self.assertRedirects(response, f'/todo/lists/{mylist.id}/')


