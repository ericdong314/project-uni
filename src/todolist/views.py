from django.shortcuts import render, redirect

from .models import Item


# Create your views here.
def home_page(request):
    if request.method == 'POST':
        text = request.POST['item_text']
        Item.objects.create(text=text)
        return redirect('/todo/lists/the-ultimate-list/')
    return render(request, 'home.html')


def list_view(request):
    context = {'item_list': Item.objects.all()}
    return render(request, 'list.html', context=context)
