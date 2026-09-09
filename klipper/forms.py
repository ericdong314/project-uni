from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('link',)

    def clean_link(self):
        link = self.cleaned_data['link']
        return link