from todolist.models import Item
from django import forms
from django.forms import widgets

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': widgets.TextInput(attrs={'placeholder': 'Enter a to-do item',
                                             'class': 'form-control form-control-lg'})
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
