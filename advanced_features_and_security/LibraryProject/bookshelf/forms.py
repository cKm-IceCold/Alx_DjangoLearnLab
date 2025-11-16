# bookshelf/forms.py

from django import forms
from .models import Book # Import the model to base the form on

class ExampleForm(forms.ModelForm):
    """
    A simple form, defined as ExampleForm, used to demonstrate secure handling 
    of user input and validation before saving to the database.
    """
    class Meta:
        model = Book
        # Include fields that were defined in the Book model
        fields = ['title', 'isbn'] 
        
    # Custom validation can be added here, ensuring input is safe
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if 'malicious' in title.lower():
    #         raise forms.ValidationError("Input cannot contain malicious keywords.")
    #     return title