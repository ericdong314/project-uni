from django.urls import path

from . import views

app_name = 'todolist'
urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/the-ultimate-list/', views.list_view, name='view_list'),
]
