from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Book
from .serializers import BookSerializer

# List all books with filtering and search capabilities
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

# Retrieve a single book by id
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Create a new book with custom validation and permission checks
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Custom method to validate and handle form submissions
    def perform_create(self, serializer):
        # Additional validation before saving
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be authenticated to create a book.")
        
        # Save the book with the current user as metadata (if needed)
        serializer.save()

# Update an existing book with custom validation
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    # Custom method to handle updates with validation
    def perform_update(self, serializer):
        # Validate that only authenticated users can update
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be authenticated to update a book.")
        
        # Optional: Add logging or additional checks before saving
        serializer.save()
    
    # Override get_queryset to add custom filtering if needed
    def get_queryset(self):
        queryset = super().get_queryset()
        # Example: filter by publication year if query parameter is provided
        year = self.request.query_params.get('year', None)
        if year is not None:
            queryset = queryset.filter(publication_year=year)
        return queryset

# Delete a book with permission and validation checks
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
    
    # Custom method to handle deletion with validation
    def perform_destroy(self, instance):
        # Additional validation before deletion
        if not self.request.user.is_staff:
            raise PermissionDenied("Only staff members can delete books.")
        
        # Delete the book
        instance.delete()
