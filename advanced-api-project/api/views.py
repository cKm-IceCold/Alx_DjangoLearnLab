from django.shortcuts import render
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer

# List all books with advanced filtering, search, and ordering capabilities
class BookListView(generics.ListAPIView):
    """
    ListView for Book model with advanced query capabilities.
    
    Features:
    - Filtering by title, author, and publication_year
    - Full-text search on title and author name
    - Ordering by title, publication_year, and author
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Step 1: Set Up Filtering
    # DjangoFilterBackend allows filtering by specific fields (title, author, publication_year)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Specify fields that can be filtered
    filterset_fields = ['title', 'author', 'publication_year']
    
    # Step 2: Implement Search Functionality
    # SearchFilter enables text search on title and author fields
    search_fields = ['title', 'author__name']
    
    # Step 3: Configure Ordering
    # OrderingFilter allows sorting by specified fields
    ordering_fields = ['title', 'publication_year', 'author']
    ordering = ['title']  # Default ordering by title

# Retrieve a single book by id
class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single Book instance by ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Create a new book with custom validation and permission checks
class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding new Book instances.
    Requires user authentication.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Custom method to validate and handle form submissions
    def perform_create(self, serializer):
        # Additional validation before saving
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be authenticated to create a book.")
        
        # Save the book
        serializer.save()

# Update an existing book with custom validation
class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying existing Book instances.
    Requires user authentication.
    Supports optional year-based filtering via query parameter.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    # Custom method to handle updates with validation
    def perform_update(self, serializer):
        # Validate that only authenticated users can update
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be authenticated to update a book.")
        
        # Save the updated book
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
    """
    DeleteView for removing Book instances.
    Requires admin/staff user privileges.
    """
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
