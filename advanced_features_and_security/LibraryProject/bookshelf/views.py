# bookshelf/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden # Good practice for 403 handling

from .models import Book # Assuming Book model is defined in models.py

# Note on Custom Permission Check:
# We use the format 'app_label.permission_codename', e.g., 'bookshelf.can_create'.
# Setting raise_exception=True ensures Django returns a 403 Forbidden page 
# if the user does not have the required permission.

def book_list(request):
    """
    Displays a list of books. While it doesn't use the decorator, 
    it must return the 'books' queryset for template rendering.
    """
    # Use permission check here if ALL viewing must be restricted:
    # if not request.user.has_perm('bookshelf.can_view'):
    #     return HttpResponseForbidden()
        
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    Restricts access to users with the 'can_create' permission (Editors/Admins).
    """
    if request.method == 'POST':
        # Placeholder logic for form handling and saving
        # form = BookForm(request.POST)
        # if form.is_valid():
        #     form.save()
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})


@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    Restricts access to users with the 'can_edit' permission (Editors/Admins).
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # Placeholder logic for form handling and saving
        # form = BookForm(request.POST, instance=book)
        # if form.is_valid():
        #     form.save()
        return redirect('book_list')
        
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})


@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    Restricts access to users with the 'can_delete' permission (Admins only).
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
        
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})