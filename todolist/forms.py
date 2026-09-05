from django import forms
from .models import Item


# class CreateItemForm(forms.Form):
#     name = forms.CharField(max_length=256)
#     details = forms.CharField(max_length=1024)
#
#     def clean_name(self):
#         name = self.cleaned_data['name']
#         ...
#         return name

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'details']
        labels = {'details': 'Description'}
        help_texts = {'details': 'Add more info about your item. (Optional)'}

    def clean_name(self):
        name = self.cleaned_data['name']
        ...
        return name