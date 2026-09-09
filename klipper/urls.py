from django.urls import path
from .views import home_page

urlpatterns = [
    path('', home_page, name='home-page'),
    path('create/', home_page, name='item-create'),
]
