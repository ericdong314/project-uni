from django.shortcuts import render, redirect

from .models import Item, List


# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def list_view(request, list_id):
    context = {'item_list': Item.objects.filter(list_id=list_id)}
    return render(request, 'list.html', context=context)


def create_view(request):
    the_list = List.objects.create()
    text = request.POST['item_text']
    Item.objects.create(text=text, list=the_list)
    return redirect(f'/todo/lists/{the_list.id}/')
