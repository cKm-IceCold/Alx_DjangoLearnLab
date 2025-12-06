from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, Post

def posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/posts.html', {'posts': posts})


# Extended registration form with email field
class RegisterForm(UserCreationForm):
    """
    Custom registration form that extends Django's UserCreationForm.
    Adds email field to the standard username and password fields.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

# Profile update form
class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'phone_number', 'location', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tell us about yourself'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    """
    Form for updating user basic information.
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

# Registration view
def register(request):
    """
    Handle user registration with email.
    GET: Display registration form
    POST: Process form submission and create new user
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'blog/register.html', {'form': form, 'errors': form.errors})
    else:
        form = RegisterForm()
    
    return render(request, 'blog/register.html', {'form': form})

# Login view
def login_view(request):
    """
    Handle user login.
    GET: Display login form
    POST: Authenticate user and log them in
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'blog/login.html')

# Logout view
def logout_view(request):
    """
    Handle user logout.
    Logs out the user and redirects to home page.
    """
    logout(request)
    return redirect('home')

# Profile view (requires login)
@login_required(login_url='login')
def profile(request):
    """
    Display user profile information including extended profile details.
    Requires user to be authenticated.
    """
    user_profile = request.user.profile
    return render(request, 'blog/profile.html', {
        'user': request.user,
        'profile': user_profile
    })

# Update profile view
@login_required(login_url='login')
def update_profile(request):
    """
    Allow user to update their profile information.
    GET: Display profile update form
    POST: Process form submission and update user and profile data
    """
    user_profile = request.user.profile
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    return render(request, 'blog/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': user_profile
    })
