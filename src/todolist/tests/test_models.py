from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from todolist.models import List, Item


class ItemModelTest(TestCase):
    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        mylist = List.objects.create()
        item = Item.objects.create(list=mylist)
        self.assertIn(item, mylist.item_set.all())

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

    def test_item_duplication_NOT_allowed(self):
        funny_text = "Please don't laugh!"
        mylist = List.objects.create()
        Item.objects.create(text=funny_text, list=mylist)
        with self.assertRaises(ValidationError) as cm:
            item = Item(text=funny_text, list=mylist)
            item.full_clean()

    def test_CAN_save_same_item_to_different_lists(self):
        funny_text = "Please don't laugh!"
        mylist = List.objects.create()
        urlist = List.objects.create()
        Item.objects.create(text=funny_text, list=mylist)
        item = Item(text=funny_text, list=urlist)
        item.full_clean()  # should not raise


class ListModelTest(TestCase):
    def test_get_absolute_url(self):
        mylist = List.objects.create()
        self.assertEqual(mylist.get_absolute_url(), f'/todo/lists/{mylist.id}/')
