from rest_framework import serializers
from .models import Book, Author
from datetime import date

# BookSerializer
# Purpose: Convert Book model instances to/from JSON for API responses and requests
# - Serialization: converts Django Book objects to JSON format for API responses
# - Deserialization: converts incoming JSON data to Book model instances for database storage
# - Validation: ensures data integrity before saving to the database
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']

    # Custom validation method
    # Purpose: ensures publication_year is not set to a future date
    # Raises ValidationError if the year is greater than the current year
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
   class Meta:
      model = Author
      fields = ['id', 'name']