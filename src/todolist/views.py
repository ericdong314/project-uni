from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from .models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'todolist/home.html')


def view_list(request, list_id):
    context = {'list': List.objects.get(pk=list_id)}
    return render(request, 'todolist/list.html', context=context)


def new_list(request):
    nulist = List.objects.create()
    text = request.POST['item_text']
    item = Item(text=text, list=nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete()
        return render(request, 'todolist/home.html', context={'error':  "You can't have an empty list item"})
    return redirect(f'/todo/lists/{nulist.id}/')


def add_list_item(request, list_id):
    text = request.POST['item_text']
    Item.objects.create(text=text, list_id=list_id)
    return redirect(f'/todo/lists/{list_id}/')
