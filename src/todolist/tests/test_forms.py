from django.test import TestCase

from todolist.forms import ItemForm, ExistingListItemForm, EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR
from todolist.models import List, Item


class ItemFormTest(TestCase):
    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_handles_save_item_to_list(self):
        mylist = List.objects.create()
        form = ItemForm(data={'text': 'do me!'})
        self.assertTrue(form.is_valid())
        new_item = form.save(for_list=mylist)
        self.assertEqual(new_item, Item.objects.get())
        self.assertEqual(new_item.text, 'do me!')
        self.assertEqual(new_item.list, mylist)

class ExistingListItemFormTest(TestCase):
    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={"text": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="no twins!")
        form = ExistingListItemForm(for_list=list_, data={"text": "no twins!"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["text"], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text':'bam!'})
        self.assertTrue(form.is_valid())
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.get())
