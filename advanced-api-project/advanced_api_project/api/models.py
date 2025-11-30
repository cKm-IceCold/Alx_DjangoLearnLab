from django.db import models

# Author Model
# Purpose: Store information about book authors
# Fields:
#   - name: CharField to store the author's name (max 100 characters)
# Methods:
#   - __str__: Returns the author's name for readable representation in admin panel and queries
class Author(models.Model):
   name = models.CharField(max_length=100)
     
   def __str__(self):
       return self.name

# Book Model
# Purpose: Store information about books and link them to their authors
# Fields:
#   - title: CharField to store the book's title (max 100 characters)
#   - publication_year: IntegerField to store the year the book was published
#   - author: ForeignKey relationship to Author model
#     * on_delete=models.CASCADE: if an author is deleted, all their books are deleted too
#     * related_name='books': allows reverse access from Author to their books (author.books.all())
# Methods:
#   - __str__: Returns the book's title for readable representation in admin panel and queries
class Book(models.Model):
      title = models.CharField(max_length=100)
      publication_year = models.IntegerField()
      author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

      def __str__(self):
          return self.title