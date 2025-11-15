# Create your models here.
from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Author(models.Model):
    """
    Represents an author of a book.

    This model maps to a table called 'Author' in the database 'NewLibrary'.
    The table will have one attribute:
        - name: A string representing the author's name (max length: 100).
    """
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
    

class Book(models.Model):
    """
    Represents a book in the library.

    This model maps to a table called 'Book' in the database 'NewLibrary'.
    The table will have two attributes:
        - title: A string representing the book's title (max length: 200).
        - author: A foreign key referencing the Author model, representing the author of the book.
                  If the referenced author is deleted, all related books will also be deleted (CASCADE).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}"

    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),           
            ('can_change_book', 'Can change book'),      
            ('can_delete_book', 'Can delete book'), 
            ] 

class Library(models.Model):
    """
    Represents a library that contains books.

    This model maps to a table called 'Library' in the database 'NewLibrary'.
    The table will have two attributes:
        - name: A string representing the library's name (max length: 200).
        - books: A many-to-many relationship with the Book model, representing the books available in the library.
                 Multiple libraries can have the same book.
    """
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='library')

    def __str__(self) -> str:
        return self.name
    

class Librarian(models.Model):
    """
    Represents a librarian who works at a library.

    This model maps to a table called 'Librarian' in the database 'NewLibrary'.
    The table will have two attributes:
        - name: A string representing the librarian's name (max length: 100).
        - library: A one-to-one relationship with the Library model, representing the library where the librarian works.
                   If the associated library is deleted, the librarian will have an unassigned Library i.e set to Null.
    """
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name
    


#creating a new user model for relationship app
# user = User.objects.create_user(username='Bob', email='',password='123yesman')
# user = User.objects.get(username='john')


# class UserProfile(models.Model):
#     class Roles(models.TextChoices):
#         admin = "Admin"
#         librarian = "Librarian"
#         member = "Member"

#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofiles')
#     role = models.CharField(max_length=20, choices=Roles, default=Roles.member)

#     def __str__(self) -> str:
#         return f"{self.user.username}'s profile."
 
from LibraryProject import settings

class UserProfile(models.Model):
    class Role(models.TextChoices):
        admin = "Admin"
        librarian = "Librarian"
        member = "Member"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(choices=Role, max_length=10, default=Role.member)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s profile. Role: {self.role}"