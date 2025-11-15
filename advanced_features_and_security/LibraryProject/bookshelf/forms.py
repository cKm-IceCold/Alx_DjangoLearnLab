from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Review
from LibraryProject import settings
from django.contrib.auth import get_user_model  # Alternatively use get_user_model()

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'review_text']
        labels = {
            'book': 'Select Book',
            'review_text': 'Your Review',
        }

class MyUserCreationForm(UserCreationForm):
        class Meta:
            model = get_user_model()
            fields = ['username', 'date_of_birth']