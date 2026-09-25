from django.urls import path

from . import views

app_name = 'todolist'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/<int:list_id>/', views.list_view, name='view_list'),
    path('lists/new/', views.create_view, name='new_item'),
]
