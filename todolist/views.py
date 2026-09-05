from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Item
from .forms import CreateItemForm

# Create your views here.

class ItemListView(generic.ListView):
    model = Item

def create_item(request):
    if request.method == 'POST':
        form = CreateItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            details = form.cleaned_data['details']
            item = Item.objects.create(name=name, details=details)
            item.save()
            return HttpResponseRedirect(reverse('items'))
    else:
        form = CreateItemForm(initial={'name': 'Change me!'})
    context = {'form':form}
    return render(request, 'create_item.html', context=context)