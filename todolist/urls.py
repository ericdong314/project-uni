from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'todolist'
urlpatterns = [
    path('', views.home_page, name='home'),
    # path('items/', views.ItemListView.as_view(), name='items'),
    # path('item/create/', views.create_item, name='create_item')
]
