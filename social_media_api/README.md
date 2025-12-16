Posts & Comments API

A RESTful API built with Django REST Framework that supports user authentication, post creation, commenting, pagination, filtering, and permission enforcement.

🚀 Base URL
http://localhost:8000/

🔐 Authentication
Register User
POST /accounts/register/


Request Body

{
  "username": "string",
  "email": "string",
  "password": "string"
}


Response

201 Created
User registered successfully

Login User
POST /accounts/login/


Request Body

{
  "username": "string",
  "password": "string"
}


Response

{
  "token": "string"
}

Authentication Header

All protected endpoints require the following header:

Authorization: Token <user_token>

📰 Posts Endpoints
List All Posts (Paginated & Searchable)
GET /posts/


Permissions

Public


Query Parameters

?page=1
?search=title_or_content


Response

{
  "count": 10,
  "next": "url",
  "previous": "url",
  "results": []
}

Create Post
POST /posts/


Permissions

Authenticated users only


Request Body

{
  "title": "string",
  "content": "string"
}


Response

201 Created

Retrieve Single Post
GET /posts/{id}/


Permissions

Public

Update Post
PUT /posts/{id}/


Permissions

Authenticated (Owner only)


Request Body

{
  "title": "string",
  "content": "string"
}

Delete Post
DELETE /posts/{id}/


Permissions

Authenticated (Owner only)


Response

204 No Content

💬 Comments Endpoints
List All Comments (Paginated)
GET /comments/


Permissions

Public


Query Parameters

?page=1

Create Comment
POST /comments/


Permissions

Authenticated users only


Request Body

{
  "post": 1,
  "content": "string"
}

Update Comment
PUT /comments/{id}/


Permissions

Authenticated (Owner only)


Request Body

{
  "content": "string"
}

Delete Comment
DELETE /comments/{id}/


Permissions

Authenticated (Owner only)


Response

204 No Content

🔒 Permissions Summary

Anyone can view posts and comments

Only authenticated users can create posts and comments

Users can only update or delete their own posts and comments

📄 Pagination

Pagination is enabled for posts and comments list endpoints.

Each paginated response includes:

count

next

previous

results

🔍 Filtering & Search

Posts can be searched using the search query parameter.

Example

GET /posts/?search=django


Search applies to:

Post title

Post content

✅ Data Integrity

Author is automatically assigned from the authenticated user

Users cannot modify or delete content they do not own

Invalid requests return appropriate HTTP status codes

🧪 Testing

All endpoints were tested using Postman to ensure:

Proper authentication

Correct permission enforcement

Data validation and integrity

🛠️ Technologies Used

Django

Django REST Framework

Token Authentication

SQLite (default)