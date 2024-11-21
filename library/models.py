from django.db import models
from django.contrib.auth.models import User  # Import the built-in User model
from datetime import date
from datetime import timedelta

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
    borrow_date = models.DateField(auto_now_add=True)  # Automatically set borrow date to today
    return_date = models.DateField(null=True, blank=True)  # Date when the book is due to be returned

    def save(self, *args, **kwargs):
        # Ensure the borrow_date is set to today if it's not already set
        if not self.borrow_date:
            from datetime import date
            self.borrow_date = date.today()
        if not self.return_date:  # Set return_date if it isn't already set
            self.return_date = self.borrow_date + timedelta(days=7)
        super().save(*args, **kwargs)


    def return_book(self):
        """Handles returning a book."""
        self.book.availability = True  # Mark the book as available
        self.book.save()  # Save the updated book status
        self.delete()
        
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title} on {self.borrow_date}"

