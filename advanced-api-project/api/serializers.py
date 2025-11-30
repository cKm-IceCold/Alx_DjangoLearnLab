from rest_framework import serializers
from .models import Book, Author
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    # accept author as an ID when creating/updating
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
   
# AuthorSerializer
# Purpose: Convert Author model instances to/from JSON for API responses and requests
# - Serialization: converts Django Author objects to JSON format for API responses
# - Deserialization: converts incoming JSON data to Author model instances for database storage

class AuthorSerializer(serializers.ModelSerializer):
    # include related books as a read-only list using the BookSerializer
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id','name',]