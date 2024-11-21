from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import *

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']

    def borrowed_books(self, obj):
        # Query BorrowRecord to get books borrowed by this user
        borrow_records = BorrowRecord.objects.filter(user=obj)
        if borrow_records.exists():
            return ", ".join([record.book.title for record in borrow_records])
        return "No books borrowed"

    borrowed_books.short_description = "Borrowed Books"

    # Add the borrowed_books method to the user detail view
    list_display = ['username', 'borrowed_books']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(BorrowRecord)
