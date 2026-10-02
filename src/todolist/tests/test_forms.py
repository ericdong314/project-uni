from django.test import TestCase

from todolist.forms import ItemForm, EMPTY_ITEM_ERROR
from todolist.models import List, Item


class ItemFormTest(TestCase):
    def test_form_renders__input(self):
        form = ItemForm()
        rendered = form.as_p()
        self.assertIn('placeholder="Enter a to-do item"', rendered)
        self.assertIn('class="form-control form-control-lg"', rendered)

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_handles_save_item_to_list(self):
        mylist = List.objects.create()
        form = ItemForm(data={'text': 'do me!'})
        new_item = form.save(for_list=mylist)
        self.assertEqual(new_item, Item.objects.get())
        self.assertEqual(new_item.text, 'do me!')
        self.assertEqual(new_item.list, mylist)
