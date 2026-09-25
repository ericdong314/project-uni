from django.shortcuts import render, redirect

from .models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    context = {'list': List.objects.get(pk=list_id)}
    return render(request, 'list.html', context=context)


def new_list(request):
    the_list = List.objects.create()
    text = request.POST['item_text']
    Item.objects.create(text=text, list=the_list)
    return redirect(f'/todo/lists/{the_list.id}/')


def add_list_item(request, list_id):
    text = request.POST['item_text']
    Item.objects.create(text=text, list_id=list_id)
    return redirect(f'/todo/lists/{list_id}/')
