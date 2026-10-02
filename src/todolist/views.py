from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .forms import ItemForm
from .models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'todolist/home.html', {'form': ItemForm()})


def view_list(request, list_id):
    our_list = List.objects.get(pk=list_id)
    error = None

    if request.method == 'POST':
        text = request.POST['text']
        item = Item(text=text, list_id=list_id)
        try:
            item.full_clean()
            item.save()
            return redirect(our_list)
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'todolist/list.html', {'list': our_list, 'error': error, 'form': ItemForm()})


def new_list(request):
    nulist = List.objects.create()
    text = request.POST['text']
    item = Item(text=text, list=nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete()
        return render(request, 'todolist/home.html', context={'error': "You can't have an empty list item"})
    return redirect(nulist)
