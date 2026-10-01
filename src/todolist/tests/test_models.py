import lxml.html
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from todolist.models import List, Item


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

    def test_cannot_save_null_list_items(self):
        mylist = List.objects.create()
        item = Item(list=mylist, text=None)
        with self.assertRaises(IntegrityError) as cm:
            item.save()

    def test_cannot_save_empty_list_item(self):
        mylist = List.objects.create()
        item = Item(list=mylist, text='')
        with self.assertRaises(ValidationError) as cm:
            item.full_clean()

    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f'/todo/lists/{mylist.id}/')