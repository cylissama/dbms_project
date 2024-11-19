from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_user, name='register_user'),
    path('add-book/', add_book, name='add_book'),
    ]
