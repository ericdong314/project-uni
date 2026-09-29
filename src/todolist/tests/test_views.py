import lxml.html
from django.test import TestCase
from todolist.models import List, Item


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/todo/')
        self.assertTemplateUsed(response, 'todolist/home.html')

    def test_renders_homepage_content(self):
        response = self.client.get('/todo/')
        self.assertContains(response, 'To-Do')

    def test_renders_input_form(self):
        response = self.client.get("/todo/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=post]")
        self.assertEqual(form.get("action"), "/todo/lists/new/")
        inputs = parsed.cssselect("input")
        self.assertIn("item_text", [input.get("name") for input in inputs])


class ListViewTest(TestCase):
    def test_uses_list_view_template(self):
        my_list = List.objects.create()
        response = self.client.get(f'/todo/lists/{my_list.id}/')
        self.assertTemplateUsed(response, 'todolist/list.html')

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/todo/lists/{mylist.id}/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=post]")
        self.assertEqual(form.get('action'), f"/todo/lists/{mylist.id}/add_item/")
        inputs = parsed.cssselect("input")
        self.assertIn('item_text', [input.get("name") for input in inputs])

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
