from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Item
from .forms import ItemForm


# Create your views here.

def home_page(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            Item.objects.create(link=link)
            return HttpResponseRedirect(reverse('home-page'))
    else:
        form = ItemForm()

    items = Item.objects.order_by('id')
    context = {'item_list': items, 'form': form}
    return render(request, 'home.html', context)
