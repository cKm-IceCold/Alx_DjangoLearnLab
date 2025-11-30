from rest_framework import serializers
from .models import Book, Author
from datetime import date

# BookSerializer converts Book model instances to/from JSON for API responses
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year']

    # Custom validation: ensures publication_year is not in the future
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"Publication year cannot be in the future. Current year is {current_year}."
            )
        return value
   
# AuthorSerializer converts Author model instances to/from JSON for API responses
class AuthorSerializer(serializers.ModelSerializer):
   class Meta:
      model = Author
      fields = ['name']
