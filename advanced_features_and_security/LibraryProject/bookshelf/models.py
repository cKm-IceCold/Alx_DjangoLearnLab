# bookshelf/models.py (Ensure this content is correct)

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

# --- Custom User Manager (Step 3) ---
class CustomUserManager(BaseUserManager):
    # ... (content from previous step for create_user and create_superuser) ...
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if 'date_of_birth' not in extra_fields:
            extra_fields['date_of_birth'] = timezone.now().date()
            
        return self.create_user(email, password, **extra_fields)


# --- Custom User Model (Step 1) ---
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        verbose_name='Date of Birth'
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/', 
        null=True, 
        blank=True, 
        verbose_name='Profile Photo'
    )

    email = models.EmailField(unique=True, blank=False)
    username = None 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth'] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email

# NOTE: If you decide to add a Book model later, it would go here:
# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     # ... other fields