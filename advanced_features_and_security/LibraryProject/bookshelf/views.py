# bookshelf/views.py (Secure Data Access)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book 

# Import necessary modules for form validation (if you use forms)
from django import forms # Hypothetical form

# Secure Search Example (Prevents SQL Injection):
def book_list(request):
    """
    Retrieves books using the ORM's filter() method, which automatically 
    parameterizes the query, preventing SQL injection.
    """
    query = request.GET.get('q')
    
    if query:
        # SECURE: Using the ORM (filter) ensures input is treated as data, not code.
        books = Book.objects.filter(title__icontains=query) 
        
        # INSECURE EXAMPLE (DON'T DO THIS):
        # books = Book.objects.raw(f"SELECT * FROM bookshelf_book WHERE title LIKE '%%{query}%%'")
    else:
        books = Book.objects.all()

    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

# NOTE ON DOCUMENTATION: All data access uses the Django ORM's methods (filter, get, all). 
# This automatically handles SQL parameterization, which is the primary defense against 
# SQL injection attacks. Direct string concatenation of user input into raw SQL is avoided.
# User input validation should be enforced via Django Forms or serializers before saving data.
# ... (book_create, book_edit, book_delete views remain the same as previous task) ...