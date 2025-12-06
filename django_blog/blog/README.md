# Django Blog Authentication System Documentation

## Overview
This documentation covers the complete authentication system for the Django Blog project, including user registration, login, logout, and profile management features.

---

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Components](#components)
3. [Authentication Flow](#authentication-flow)
4. [User Registration](#user-registration)
5. [User Login](#user-login)
6. [User Profile Management](#user-profile-management)
7. [Testing Guide](#testing-guide)
8. [Troubleshooting](#troubleshooting)

---

## System Architecture

### Overview Diagram
```
User Registration → User Model Created → UserProfile Auto-Created → Login Available
    ↓
User Login → Session Created → Authenticated User → Profile Access
    ↓
Profile Management → Update User/Profile Data → Save to Database
    ↓
User Logout → Session Destroyed → Redirect to Home
```

### Technology Stack
- **Framework**: Django 4.x
- **Authentication**: Django's built-in `django.contrib.auth`
- **Database**: SQLite (default)
- **Frontend**: HTML with Tailwind CSS
- **Image Handling**: Pillow library

---

## Components

### 1. Models

#### UserProfile Model
Extends Django's User model with additional profile information.

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    website = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Fields:**
- `user`: Foreign key to Django User model (one-to-one)
- `bio`: User biography (up to 500 characters)
- `profile_picture`: User's avatar image
- `phone_number`: Contact phone number
- `location`: Geographic location (city, country)
- `website`: Personal or business website URL
- `created_at`: Profile creation timestamp
- `updated_at`: Last profile update timestamp

---

### 2. Forms

#### RegisterForm
Extends Django's UserCreationForm with email field.

```python
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

**Validation:**
- Username: unique, alphanumeric (required)
- Email: valid email format (required)
- Password1: minimum 8 characters, not common passwords
- Password2: must match password1

#### UserForm
For updating basic user information.

```python
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
```

#### UserProfileForm
For updating extended profile information.

```python
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'phone_number', 'location', 'website']
```

---

### 3. Views

#### register(request)
**Purpose**: Handle user registration

**URL**: `/blog/register/`

**Methods**: GET, POST

**Behavior**:
- GET: Display empty registration form
- POST: Validate form and create new user
- Auto-creates UserProfile via Django signal
- Auto-logs in user after successful registration

**Flow**:
```
User submits form → Validate username/email uniqueness → Hash password → 
Create User object → Signal creates UserProfile → Login user → Redirect to profile
```

#### login_view(request)
**Purpose**: Authenticate user and create session

**URL**: `/blog/login/`

**Methods**: GET, POST

**Behavior**:
- GET: Display login form
- POST: Authenticate credentials and create session
- Sets session cookie in browser
- Redirects to profile page on success

**Validation**:
- Username must exist
- Password must match user's hashed password

#### logout_view(request)
**Purpose**: Destroy user session

**URL**: `/blog/logout/`

**Methods**: GET

**Behavior**:
- Destroys session cookie
- Clears authentication credentials
- Redirects to home page

#### profile(request)
**Purpose**: Display user's profile information

**URL**: `/blog/profile/`

**Methods**: GET

**Requirements**: User must be authenticated

**Decorator**: `@login_required(login_url='login')`

**Data displayed**:
- Username
- Full name (first + last)
- Email address
- Phone number
- Location
- Website
- Bio
- Profile picture
- Member since date

#### update_profile(request)
**Purpose**: Allow user to edit profile information

**URL**: `/blog/profile/update/`

**Methods**: GET, POST

**Requirements**: User must be authenticated

**Behavior**:
- GET: Display pre-filled profile update form
- POST: Update both User and UserProfile models
- Supports file upload for profile picture
- Redirects to profile view on success

**Data that can be updated**:
- Email
- First name
- Last name
- Bio
- Phone number
- Location
- Website
- Profile picture

---

### 4. Signals

#### create_user_profile Signal
Automatically creates a UserProfile when a new User is created.

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

**Trigger**: When User object is created

**Action**: Creates empty UserProfile linked to the new User

---

### 5. Templates

#### register.html
Registration page with form for new users.

**Elements**:
- Username input
- Email input
- Password input
- Confirm password input
- Register button
- Link to login page
- Error messages display

#### login.html
Login page for existing users.

**Elements**:
- Username input
- Password input
- Login button
- Link to registration page
- Error message display

#### profile.html
User's profile display page.

**Elements**:
- Profile picture/avatar
- User's full name
- Username
- Email address
- Phone number
- Location
- Website link
- Bio text
- Member since date
- Edit Profile button
- Logout button
- Back to Home button

#### update_profile.html
Profile editing page.

**Form Sections**:
1. Basic Information
   - Email
   - First name
   - Last name

2. Profile Details
   - Profile picture upload
   - Bio textarea
   - Phone number
   - Location
   - Website URL

**Elements**:
- Save Changes button
- Cancel button
- Current profile picture display

---

## Authentication Flow

### User Registration Flow
```
1. User visits /blog/register/
2. System displays RegisterForm
3. User fills in username, email, password
4. User submits form
5. System validates:
   - Username is unique
   - Email is unique and valid format
   - Passwords match
   - Password meets requirements
6. If valid:
   - User object created in database
   - Password is hashed (PBKDF2 algorithm)
   - Django signal triggers
   - UserProfile object created automatically
   - User session created
   - User redirected to profile page
7. If invalid:
   - Form re-displayed with error messages
```

### User Login Flow
```
1. User visits /blog/login/
2. System displays login form
3. User enters username and password
4. User submits form
5. System authenticates:
   - Checks if username exists
   - Hashes provided password
   - Compares with stored hash
6. If credentials valid:
   - Session created
   - Session ID stored in cookie
   - User redirected to profile
7. If credentials invalid:
   - Error message displayed
   - Form re-displayed
```

### Session Management
```
Browser sends request → Django checks session cookie → 
Matches against session database → Retrieves User object → 
Request.user is populated → Access to user data available
```

### Protected View Access
```
User requests /blog/profile/ →
Django checks @login_required decorator →
If not authenticated, redirect to /blog/login/ →
If authenticated, render profile page with user data
```

---

## User Registration

### Step-by-Step Guide

**1. Navigate to Registration Page**
```
URL: http://localhost:8000/blog/register/
```

**2. Fill Registration Form**
- **Username**: Choose unique username (alphanumeric, underscores allowed)
- **Email**: Enter valid email address
- **Password**: Enter strong password (8+ characters recommended)
- **Confirm Password**: Re-enter password to verify

**3. Submit Form**
Click "Create Account" button

**4. Validation**
System checks:
- Username doesn't already exist
- Email doesn't already exist
- Email is valid format
- Passwords match
- Password meets security requirements

**5. Account Creation**
- User account created
- UserProfile created automatically
- Session started
- User logged in
- Redirected to profile page

**6. Profile Complete**
User can now:
- View their profile
- Update profile information
- Access protected pages
- Logout

---

## User Login

### Step-by-Step Guide

**1. Navigate to Login Page**
```
URL: http://localhost:8000/blog/login/
```

**2. Enter Credentials**
- **Username**: Enter registered username
- **Password**: Enter associated password

**3. Submit Form**
Click "Login" button

**4. Authentication**
System checks:
- Username exists in database
- Password hash matches stored hash

**5. Session Creation**
- Session cookie created
- Session data stored in database
- User authenticated for duration of session

**6. Redirect**
User directed to profile page

### Session Duration
- Default session timeout: 2 weeks
- Configurable in settings.py: `SESSION_COOKIE_AGE`

---

## User Profile Management

### Viewing Profile

**1. Navigate to Profile**
```
URL: http://localhost:8000/blog/profile/
Requires: User must be logged in
```

**2. Information Displayed**
- Profile picture (if uploaded)
- Username
- Full name
- Email
- Phone number
- Location
- Website
- Bio
- Member since date

**3. Available Actions**
- Click "Edit Profile" to update information
- Click "Logout" to end session
- Click "Back to Home" to return to home page

### Updating Profile

**1. Navigate to Edit Profile**
```
URL: http://localhost:8000/blog/profile/update/
Requires: User must be logged in
```

**2. Update Basic Information**
- Email address
- First name
- Last name

**3. Update Profile Details**
- Upload new profile picture (JPG, PNG, GIF)
- Write or edit bio (max 500 characters)
- Add phone number
- Add location
- Add website URL

**4. Save Changes**
Click "Save Changes" button

**5. Verification**
- Form validates all inputs
- Profile picture file type checked
- Email checked for uniqueness
- Website URL format validated

**6. Update Complete**
- Data saved to database
- User redirected to profile page
- Changes immediately visible

### Deleting Profile Picture
```
1. Navigate to /blog/profile/update/
2. In Profile Picture field, click "Clear"
3. Click "Save Changes"
4. Profile picture removed
5. Default avatar displayed on profile page
```

---

## Testing Guide

### Prerequisites
```bash
# Install dependencies
pip install django pillow

# Navigate to project
cd django_blog

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Server runs at: `http://localhost:8000`

---

### Test 1: User Registration

**Test Case 1.1: Successful Registration**

```
Steps:
1. Navigate to http://localhost:8000/blog/register/
2. Enter username: "testuser1"
3. Enter email: "testuser1@example.com"
4. Enter password: "SecurePass123!"
5. Confirm password: "SecurePass123!"
6. Click "Create Account"

Expected Result:
- No error messages displayed
- Redirected to profile page
- Username "testuser1" displayed on profile
- Email "testuser1@example.com" displayed
- "Member since" shows current date
- Can click "Edit Profile" button
```

**Test Case 1.2: Duplicate Username**

```
Steps:
1. Register user "testuser1" (from test 1.1)
2. Try to register again with same username
3. Enter different email and password

Expected Result:
- Error message: "A user with that username already exists"
- Form re-displayed
- User not created
```

**Test Case 1.3: Duplicate Email**

```
Steps:
1. Register user with email "test@example.com"
2. Register new user with same email but different username

Expected Result:
- Error message appears
- Form re-displayed
- Second user not created
```

**Test Case 1.4: Password Mismatch**

```
Steps:
1. Enter username: "testuser2"
2. Enter password: "Pass123!"
3. Confirm password: "DifferentPass123"
4. Click "Create Account"

Expected Result:
- Error message: "The two password fields didn't match"
- Form re-displayed
- User not created
```

**Test Case 1.5: Weak Password**

```
Steps:
1. Enter username: "testuser3"
2. Enter password: "password"
3. Confirm password: "password"
4. Click "Create Account"

Expected Result:
- Error message about password being too common
- Form re-displayed
- User not created
```

---

### Test 2: User Login

**Test Case 2.1: Successful Login**

```
Steps:
1. Register user: username "logintest", password "TestPass123!"
2. Logout (if still logged in)
3. Navigate to http://localhost:8000/blog/login/
4. Enter username: "logintest"
5. Enter password: "TestPass123!"
6. Click "Login"

Expected Result:
- No error messages
- Redirected to profile page
- Username displayed on profile
- "Edit Profile" button visible
- "Logout" button visible
```

**Test Case 2.2: Wrong Password**

```
Steps:
1. Navigate to login page
2. Enter correct username
3. Enter wrong password
4. Click "Login"

Expected Result:
- Error message: "Invalid username or password"
- Form re-displayed
- User not logged in
- Not redirected to profile
```

**Test Case 2.3: Non-existent Username**

```
Steps:
1. Navigate to login page
2. Enter non-existent username: "nonexistent123"
3. Enter any password
4. Click "Login"

Expected Result:
- Error message: "Invalid username or password"
- Form re-displayed
- User not logged in
```

**Test Case 2.4: Case Sensitivity**

```
Steps:
1. Register user with username: "TestUser"
2. Try login with username: "testuser" (lowercase)

Expected Result:
- Username comparison should be case-insensitive
- Login successful
- User redirected to profile
```

---

### Test 3: Protected Pages (Login Required)

**Test Case 3.1: Access Profile Without Login**

```
Steps:
1. Clear browser cookies (logout)
2. Navigate to http://localhost:8000/blog/profile/

Expected Result:
- Redirected to login page
- URL shows: http://localhost:8000/blog/login/?next=/blog/profile/
```

**Test Case 3.2: Access Update Profile Without Login**

```
Steps:
1. Clear browser cookies (logout)
2. Navigate to http://localhost:8000/blog/profile/update/

Expected Result:
- Redirected to login page
- URL shows: http://localhost:8000/blog/login/?next=/blog/profile/update/
```

**Test Case 3.3: Redirect After Login**

```
Steps:
1. Navigate to /blog/profile/ (without login)
2. Redirected to login page
3. Login with valid credentials
4. Check current URL

Expected Result:
- User redirected back to /blog/profile/
- User's profile displayed
```

---

### Test 4: User Logout

**Test Case 4.1: Logout Functionality**

```
Steps:
1. Login as user
2. Navigate to profile page
3. Click "Logout" button

Expected Result:
- Redirected to home page
- Session destroyed
- Cookies cleared
- Cannot access /blog/profile/ without logging in again
```

**Test Case 4.2: Session Invalidation**

```
Steps:
1. Login as user (note session ID from browser dev tools)
2. Click "Logout"
3. Open dev tools → Application → Cookies
4. Check sessionid cookie

Expected Result:
- Session cookie removed
- Previous session ID invalid
- New login creates new session ID
```

---

### Test 5: Profile Management

**Test Case 5.1: View Profile Information**

```
Steps:
1. Login as user
2. Navigate to /blog/profile/

Expected Result:
- Username displayed
- Email displayed
- Full name displayed (if set)
- Location displayed (if set)
- Phone displayed (if set)
- Bio displayed (if set)
- Website link (if set)
- Member since date shown
- Profile picture displayed (if uploaded)
```

**Test Case 5.2: Update Basic Information**

```
Steps:
1. Login as user
2. Navigate to /blog/profile/update/
3. Change first name: "John"
4. Change last name: "Doe"
5. Change email: "john.doe@example.com"
6. Click "Save Changes"

Expected Result:
- Form submitted
- No error messages
- Redirected to profile page
- New information displayed on profile
- Email changed to "john.doe@example.com"
- Full name shows "John Doe"
```

**Test Case 5.3: Upload Profile Picture**

```
Steps:
1. Navigate to /blog/profile/update/
2. Click on "Profile Picture" file input
3. Select image file (JPG, PNG, GIF)
4. Click "Save Changes"

Expected Result:
- Image uploaded
- File stored in /media/profile_pictures/
- Profile page displays new image
- Image appears as circular avatar
```

**Test Case 5.4: Update Bio**

```
Steps:
1. Navigate to /blog/profile/update/
2. Enter bio: "Software developer from California"
3. Click "Save Changes"

Expected Result:
- Bio saved (max 500 characters)
- Displayed on profile page
- Preserved across sessions
```

**Test Case 5.5: Add Location**

```
Steps:
1. Navigate to /blog/profile/update/
2. Enter location: "San Francisco, California"
3. Click "Save Changes"

Expected Result:
- Location saved
- Displayed on profile page
```

**Test Case 5.6: Add Phone Number**

```
Steps:
1. Navigate to /blog/profile/update/
2. Enter phone: "+1 (555) 123-4567"
3. Click "Save Changes"

Expected Result:
- Phone number saved
- Displayed on profile page
```

**Test Case 5.7: Add Website**

```
Steps:
1. Navigate to /blog/profile/update/
2. Enter website: "https://www.example.com"
3. Click "Save Changes"

Expected Result:
- Website URL saved
- Displayed on profile page as clickable link
- Link opens in new tab when clicked
```

**Test Case 5.8: Invalid Email Format**

```
Steps:
1. Navigate to /blog/profile/update/
2. Enter email: "invalidemail"
3. Click "Save Changes"

Expected Result:
- Error message: "Enter a valid email address"
- Form re-displayed
- Data not saved
```

**Test Case 5.9: Invalid Website URL**

```
Steps:
1. Navigate to /blog/profile/update/
2. Enter website: "not a valid url"
3. Click "Save Changes"

Expected Result:
- Error message: "Enter a valid URL"
- Form re-displayed
- Data not saved
```

**Test Case 5.10: Cancel Edit**

```
Steps:
1. Navigate to /blog/profile/update/
2. Make changes
3. Click "Cancel" button

Expected Result:
- Changes not saved
- Redirected to profile page
- Original data preserved
```

---

### Test 6: Database Integrity

**Test Case 6.1: UserProfile Auto-Creation**

```
Steps:
1. Access Django admin: http://localhost:8000/admin/
2. Navigate to Users section
3. Create new user via Django admin
4. Check UserProfile section

Expected Result:
- UserProfile automatically created for new user
- Links to correct user
- All fields have default/empty values
```

**Test Case 6.2: Profile Deletion Protection**

```
Steps:
1. Register user and set profile data
2. Access Django shell: python manage.py shell
3. Delete user: User.objects.get(username='testuser').delete()
4. Check if UserProfile still exists

Expected Result:
- UserProfile deleted with user (CASCADE delete)
- Database remains consistent
```

---

### Test 7: Security Tests

**Test Case 7.1: Password Hashing**

```
Steps:
1. Register user with password: "TestPass123!"
2. Access Django shell: python manage.py shell
3. Check password: user.password

Expected Result:
- Password is hashed (not plain text)
- Hash format: "pbkdf2_sha256$iterations$salt$hash"
- Plain password never stored
```

**Test Case 7.2: Session Security**

```
Steps:
1. Login as user
2. Open browser dev tools → Network tab
3. Make request to /blog/profile/
4. Check request headers

Expected Result:
- Session cookie included: "sessionid=..."
- CSRF token included in POST requests
- Cookies marked as HttpOnly (secure)
```

**Test Case 7.3: CSRF Protection**

```
Steps:
1. Login as user
2. Navigate to /blog/profile/update/
3. View page source (Ctrl+U)
4. Search for "csrf"

Expected Result:
- CSRF token present in HTML: {% csrf_token %}
- Token sent with form submission
- POST requests validated against token
```

**Test Case 7.4: SQL Injection Prevention**

```
Steps:
1. Navigate to login page
2. Enter username: admin' OR '1'='1
3. Enter password: anything
4. Try login

Expected Result:
- Login fails with "Invalid username or password"
- No error message leaks database structure
- Attack is prevented by parameterized queries
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: ImportError: cannot import name 'UserProfile'

**Cause**: UserProfile model not defined in models.py

**Solution**:
```python
# Ensure models.py contains:
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # ... other fields
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

#### Issue 2: ModuleNotFoundError: No module named 'PIL'

**Cause**: Pillow library not installed

**Solution**:
```bash
pip install Pillow
```

---

#### Issue 3: "No such table: auth_user"

**Cause**: Migrations not applied

**Solution**:
```bash
python manage.py migrate
```

---

#### Issue 4: Profile picture not uploading

**Cause**: Media files directory not configured

**Solution**:
```python
# In settings.py, ensure:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# In urls.py, add:
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... existing urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

#### Issue 5: "You are not authenticated" but logged in

**Cause**: Session cookie expired or invalid

**Solution**:
```bash
# Clear browser cookies and login again
# Or check SESSION_COOKIE_AGE in settings.py (default 2 weeks)
```

---

#### Issue 6: Form submission showing CSRF token missing

**Cause**: {% csrf_token %} not in template

**Solution**:
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

### Database Reset

To completely reset authentication data:

```bash
# Delete database
rm db.sqlite3

# Recreate database
python manage.py migrate

# Create new superuser (optional)
python manage.py createsuperuser
```

---

## Best Practices

### For Users
1. Use strong passwords (8+ characters, mix of letters/numbers/symbols)
2. Keep email address updated for account recovery
3. Don't share account credentials
4. Logout from public/shared computers
5. Regularly update profile information

### For Developers
1. Never store passwords in plain text
2. Always use @login_required decorator for protected views
3. Validate and sanitize all user inputs
4. Use CSRF tokens for all POST requests
5. Implement rate limiting for login attempts
6. Keep Django and dependencies updated
7. Use HTTPS in production
8. Configure secure session cookies:
   ```python
   SESSION_COOKIE_SECURE = True  # HTTPS only
   SESSION_COOKIE_HTTPONLY = True  # No JS access
   CSRF_COOKIE_SECURE = True  # HTTPS only
   ```

---

## Additional Resources

- [Django Authentication Documentation](https://docs.djangoproject.com/en/4.0/topics/auth/)
- [Django Forms Documentation](https://docs.djangoproject.com/en/4.0/topics/forms/)
- [Django Signals Documentation](https://docs.djangoproject.com/en/4.0/topics/signals/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

## Support

For issues or questions:
1. Check Django logs: `python manage.py runserver` output
2. Enable DEBUG mode to see detailed error messages
3. Use Django shell to debug: `python manage.py shell`
4. Check database with Django admin: `http://localhost:8000/admin/`
