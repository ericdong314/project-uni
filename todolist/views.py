from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Item


# Create your views here.
def home_page(request):
    if request.method == 'POST':
        text = request.POST['item_text']
        Item.objects.create(text=text)
        return redirect('todolist:home')

    context = {'item_list': enumerate(Item.objects.all(), start=1)}
    return render(request, 'home.html', context=context)
