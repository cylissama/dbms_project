from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home_view(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            user.save()
            return redirect('home')  # Redirect to the homepage after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'register_user.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to homepage after successful login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the homepage after adding the book
    else:
        form = AddBookForm()
    return render(request, 'add_book.html', {'form': form})
