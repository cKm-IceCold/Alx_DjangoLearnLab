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
    
    # PUT/PATCH /api/books/<int:pk>/update/ - Update an existing book
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    
    # DELETE /api/books/<int:pk>/delete/ - Delete a book
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]