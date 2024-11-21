from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def home_view(request):
    query = request.GET.get('q', '').strip()  # Get the search query, default to empty string
    filter_by = request.GET.get('filter_by', 'title')  # Get the filter option, default to 'title'

    books = Book.objects.all()  # Default to all books

    if query:
        if filter_by == 'book_id':
            try:
                books = books.filter(id=int(query))
            except ValueError:
                books = Book.objects.none()  # No results if Book ID is not a valid integer
        elif filter_by == 'title':
            books = books.filter(title__icontains=query)
        elif filter_by == 'author':
            books = books.filter(author__icontains=query)
        elif filter_by == 'isbn':
            books = books.filter(isbn__icontains=query)
        elif filter_by == 'published_year':
            try:
                books = books.filter(published_year=int(query))
            except ValueError:
                books = Book.objects.none()  # No results if year is not a valid integer
        elif filter_by == 'genre':
            books = books.filter(genre__icontains=query)
        elif filter_by == 'availability':
            if query.lower() in ['yes', 'true', 'available']:
                books = books.filter(availability=True)
            elif query.lower() in ['no', 'false', 'unavailable']:
                books = books.filter(availability=False)
            else:
                books = Book.objects.none()  # Invalid availability filter

    return render(request, 'home.html', {'books': books, 'query': query, 'filter_by': filter_by})

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


@staff_member_required  # Ensure only superusers or staff members can access this view
def edit_book(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home after editing
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
def borrow_book(request, book_id):
    # Get the book instance
    book = get_object_or_404(Book, book_id=book_id)

    # Check if the book is available
    if not book.availability:
        return render(request, 'borrow_book.html', {
            'error': f"Sorry, '{book.title}' is currently unavailable."
        })

    if request.method == 'POST':
        # Create the BorrowRecord for the logged-in user
        borrow_record = BorrowRecord.objects.create(
            book=book,
            user=request.user,
            borrow_date=date.today(),
        )
        # Mark the book as unavailable
        book.availability = False
        book.save()

        return redirect('home')  # Redirect to the homepage after borrowing
    else:
        return render(request, 'borrow_book.html', {'book': book})

@login_required
def return_books(request):
    # Get all borrowed books for the logged-in user that haven't been returned
    borrowed_books = BorrowRecord.objects.filter(user=request.user, return_date__isnull=True)

    if request.method == 'POST':
        # Get the BorrowRecord ID from the POST request
        borrow_record_id = request.POST.get('borrow_record_id')
        borrow_record = BorrowRecord.objects.get(id=borrow_record_id, user=request.user)

        # Return the book
        borrow_record.return_book()
        return redirect('return_books')  # Redirect to the same page after returning the book

    return render(request, 'return_books.html', {'borrowed_books': borrowed_books})
