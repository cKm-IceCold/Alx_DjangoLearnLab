# Social Media API

This project is a Django REST Framework–based social media API that supports user authentication, following users, creating posts and comments, and generating a personalized feed.

---

## 🔐 Authentication

Token-based authentication is used.

### Login
POST /api/accounts/login/

Returns an authentication token upon successful login.

---

## 👥 Follow System

### Follow a User
POST /api/accounts/follow/<user_id>/

**Auth required:** Yes  
**Description:** Follow another user.

---

### Unfollow a User
POST /api/accounts/unfollow/<user_id>/

**Auth required:** Yes  
**Description:** Unfollow a previously followed user.

---

## 📰 Feed

### Get Feed
GET /api/posts/feed/

**Auth required:** Yes  
**Description:** Returns posts created by users that the authenticated user follows, ordered by most recent.

---

## 🧱 Models Overview

### Custom User Model
- Extends `AbstractUser`
- Added field:
  - `following`: ManyToManyField to self (symmetrical=False)

```python
following = models.ManyToManyField(
    'self',
    symmetrical=False,
    related_name='followers',
    blank=True
)
