from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    # GET /api/books/ - List all books
    path('books/', BookListView.as_view(), name='book-list'),
    
    # POST /api/books/ - Create a new book
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    
    # GET /api/books/<int:pk>/ - Retrieve a single book by ID
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    
    # PUT/PATCH /api/books/update/<int:pk>/ - Update an existing book
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),
    
    # DELETE /api/books/delete/<int:pk>/ - Delete a book
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),
]