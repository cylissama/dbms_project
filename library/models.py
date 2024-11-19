from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model
from datetime import date
class Book(models.Model):
    book_id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_year = models.IntegerField()
    genre = models.CharField(max_length=100)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # ForeignKey to Book
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User
    borrow_date = models.DateField()  # Date when the book was borrowed
    return_date = models.DateField(null=True, blank=True)  # Date when the book was returned, can be null


    def return_book(self):
        # Update the book's availability
        self.book.availability = True
        self.book.save()
        self.return_date = date.today()
        self.save()

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} on {self.borrow_date}"

