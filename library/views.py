from django.shortcuts import render, redirect
from .models import Book
from .forms import *
from django.contrib.auth.models import User

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

def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the homepage after adding the book
    else:
        form = AddBookForm()
    return render(request, 'add_book.html', {'form': form})
