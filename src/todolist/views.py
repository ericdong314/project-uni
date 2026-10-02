from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .forms import ItemForm
from .models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'todolist/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    our_list = List.objects.get(pk=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save(our_list)
            return redirect(our_list)
    return render(request, 'todolist/list.html', {'list': our_list, 'form': form})


def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(nulist)
        return redirect(nulist)
    else:
        return render(request, 'todolist/home.html', context={'form': form})
