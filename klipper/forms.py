from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('link',)
        widgets = {'link': forms.TextInput(attrs={'id':'id_new_item', 'placeholder': 'Enter a URL'})}

    def clean_link(self):
        link = self.cleaned_data['link']
        return link