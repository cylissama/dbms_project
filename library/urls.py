from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_user, name='register_user'),
    path('add-book/', add_book, name='add_book'),
    path('logout/', LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    path('login/', login_user, name='login_user'),
]