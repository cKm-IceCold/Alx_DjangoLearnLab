from typing import Any
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from LibraryProject import settings

# # Create your models here.

#Creating a new Custom User Model and it's manager
class CustomUserManager(UserManager):
    def create_user(self, username: str, email: str | None = ..., password: str | None = ...,**extra_fields: Any) -> Any:
        # if not date_of_birth:
        #     raise ValueError("The date_of_birth field is required.")
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username: str, email: str | None, password: str | None,**extra_fields: Any) -> Any:
        # if not date_of_birth:
        #     raise ValueError("The date_of_birth field is required.")
        return super().create_superuser(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField()
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username




class Author(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        permissions = [
            
            ('review_author', "Can review Author")
        ]

class Book(models.Model):
    class Meta:
        permissions = [
            ('review_book', "Can review a book"),
            ('can_view', 'Can view books'),
            ('can_edit', 'Can edit a book'),
            ('can_create', "Can create a new book"),
            ("can_delete", 'Can delete a book')
        ]

    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="books")
    publication_year = models.IntegerField(default=2000)


    def __str__(self) -> str:
        return self.title
    
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_reviews")
    review_text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.book.title} by {self.user.username}"