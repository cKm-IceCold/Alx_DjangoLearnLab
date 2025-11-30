# API Views Documentation

## Overview
This document outlines the configuration and behavior of each generic view in the Book API. Each view handles a specific CRUD operation with custom validation, permission checks, and filtering capabilities.

---

## Views Configuration

### 1. BookListView
**Endpoint:** `GET /api/books/`

**Purpose:** Retrieve a list of all books with optional filtering and search capabilities.

**Configuration:**
- **Serializer:** `BookSerializer`
- **Permission:** `AllowAny` (publicly accessible)
- **Filter Backends:** 
  - `SearchFilter`: allows searching by title or author name
  - `OrderingFilter`: allows sorting by title or publication year

**Query Parameters:**
- `search=<query>` - Search books by title or author name
  - Example: `GET /api/books/?search=django`
- `ordering=<field>` - Sort results by specified field
  - Example: `GET /api/books/?ordering=-publication_year` (descending order)
  - Example: `GET /api/books/?ordering=title` (ascending order)

**Custom Behavior:** None

**Example Request:**
```
GET /api/books/?search=python&ordering=-publication_year
```

---

### 2. BookDetailView
**Endpoint:** `GET /api/books/<int:pk>/`

**Purpose:** Retrieve a single book by its ID.

**Configuration:**
- **Serializer:** `BookSerializer`
- **Permission:** `AllowAny` (publicly accessible)
- **Filter Backends:** None

**Custom Behavior:** None

**Example Request:**
```
GET /api/books/1/
```

**Response:**
```json
{
  "id": 1,
  "title": "Django for Beginners",
  "author": 1,
  "publication_year": 2023
}
```

---

### 3. BookCreateView
**Endpoint:** `POST /api/books/create/`

**Purpose:** Create a new book in the database.

**Configuration:**
- **Serializer:** `BookSerializer`
- **Permission:** `IsAuthenticatedOrReadOnly` (authenticated users can create)
- **Filter Backends:** None

**Custom Hooks:**
- **`perform_create(serializer)`**: Custom method that:
  - Validates user authentication before allowing book creation
  - Raises `PermissionDenied` if user is not authenticated
  - Saves the book to the database

**Validation:**
- User must be authenticated
- `publication_year` cannot be in the future (handled by serializer validation)

**Example Request:**
```
POST /api/books/create/
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Advanced Django",
  "author": 1,
  "publication_year": 2023
}
```

**Error Response (Unauthenticated):**
```json
{
  "detail": "You must be authenticated to create a book."
}
```

---

### 4. BookUpdateView
**Endpoint:** `PUT/PATCH /api/books/<int:pk>/update/`

**Purpose:** Update an existing book's information.

**Configuration:**
- **Serializer:** `BookSerializer`
- **Permission:** `IsAuthenticated` (only authenticated users)
- **Filter Backends:** None

**Custom Hooks:**
- **`perform_update(serializer)`**: Custom method that:
  - Validates user authentication before allowing updates
  - Raises `PermissionDenied` if user is not authenticated
  - Saves changes to the database

- **`get_queryset()`**: Overridden to support optional filtering by publication year
  - Query Parameter: `year=<value>`
  - Example: `GET /api/books/1/update/?year=2023`

**Validation:**
- User must be authenticated
- `publication_year` cannot be in the future (handled by serializer validation)

**Example Request (PUT - full update):**
```
PUT /api/books/1/update/
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Advanced Django Patterns",
  "author": 1,
  "publication_year": 2024
}
```

**Example Request (PATCH - partial update):**
```
PATCH /api/books/1/update/
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Django Advanced Topics"
}
```

---

### 5. BookDeleteView
**Endpoint:** `DELETE /api/books/<int:pk>/delete/`

**Purpose:** Delete a book from the database.

**Configuration:**
- **Serializer:** `BookSerializer`
- **Permission:** `IsAdminUser` (only admin/staff users)
- **Filter Backends:** None

**Custom Hooks:**
- **`perform_destroy(instance)`**: Custom method that:
  - Validates that only staff members can delete books
  - Raises `PermissionDenied` if user is not staff
  - Permanently removes the book from the database

**Validation:**
- User must be authenticated
- User must be a staff member

**Example Request:**
```
DELETE /api/books/1/delete/
Authorization: Bearer <token>
```

**Error Response (Non-staff user):**
```json
{
  "detail": "Only staff members can delete books."
}
```

---

## Permission Summary

| View | Method | Permission | Who Can Access |
|------|--------|-----------|-----------------|
| BookListView | GET | AllowAny | Everyone |
| BookDetailView | GET | AllowAny | Everyone |
| BookCreateView | POST | IsAuthenticatedOrReadOnly | Authenticated users |
| BookUpdateView | PUT/PATCH | IsAuthenticated | Authenticated users |
| BookDeleteView | DELETE | IsAdminUser | Staff/Admin users only |

---

## Custom Features

### 1. Search and Filter
The `BookListView` supports advanced search and ordering:
```
GET /api/books/?search=python&ordering=-publication_year
```

### 2. Year-Based Filtering
The `BookUpdateView` allows optional filtering by year:
```
GET /api/books/1/update/?year=2023
```

### 3. Publication Year Validation
The serializer ensures `publication_year` is not set to a future date.

### 4. Permission Validation
All views with custom `perform_*` methods include additional permission checks beyond the class-level `permission_classes`.

---

## Step 6 — Implementation Notes: Filtering, Searching, Ordering

Summary
- The BookListView exposes advanced query capabilities so clients can filter, search, and order Book results.
- Implementation uses DRF filter backends: `DjangoFilterBackend`, `SearchFilter`, and `OrderingFilter`.

Server-side setup
1. Install django-filter:
   ```
   pip install django-filter
   ```
2. Add to `INSTALLED_APPS` and REST config (project settings):
   ```python
   INSTALLED_APPS += ['django_filters']
   REST_FRAMEWORK['DEFAULT_FILTER_BACKENDS'] = [
       'django_filters.rest_framework.DjangoFilterBackend',
       'rest_framework.filters.SearchFilter',
       'rest_framework.filters.OrderingFilter',
   ]
   ```

How it is configured in the view
- In `api/views.py` the BookListView is configured like:
```python
# BookListView (excerpt)
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['title', 'author', 'publication_year']
search_fields = ['title', 'author__name']           # text search on title and author name
ordering_fields = ['title', 'publication_year', 'author']
ordering = ['title']                                # default ordering
```

Usage examples (query parameters)
- Filter by exact title:
  GET /api/books/?title=Django
- Filter by author id:
  GET /api/books/?author=1
- Filter by publication year:
  GET /api/books/?publication_year=2023
- Text search (title or author name):
  GET /api/books/?search=python
- Order results (ascending title):
  GET /api/books/?ordering=title
- Order results (descending publication year):
  GET /api/books/?ordering=-publication_year
- Combine filter, search and ordering:
  GET /api/books/?publication_year=2023&search=django&ordering=title

Notes and tips
- `filterset_fields` performs exact-value filtering. For more advanced lookups (contains, icontains, range), define a FilterSet class and register it on the view.
- `search` runs a simple text search across the configured `search_fields`.
- `ordering` accepts any field listed in `ordering_fields`; prefix with `-` for descending.
- Ensure serializers and model relationships (e.g., `author__name`) exist and are correct.

Testing
- Use curl/Postman to verify endpoints, include auth headers for protected endpoints.
- Example curl (search + ordering):
  ```
  curl "http://localhost:8000/api/books/?search=django&ordering=-publication_year"
  ```

End of implementation notes.

---

## Testing the API

### 1. Using cURL
```bash
# List all books
curl -X GET http://localhost:8000/api/books/

# Create a book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Django","author":1,"publication_year":2023}'

# Update a book
curl -X PATCH http://localhost:8000/api/books/1/update/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Django Advanced"}'

# Delete a book (admin only)
curl -X DELETE http://localhost:8000/api/books/1/delete/ \
  -H "Authorization: Bearer <token>"
```

### 2. Using Postman
- Create a new request for each endpoint
- Add `Authorization: Bearer <token>` header for protected endpoints
- Select appropriate HTTP method (GET, POST, PUT, PATCH, DELETE)
- Set `Content-Type: application/json` for requests with body

---

## Notes
- All endpoints return JSON responses
- Unauthenticated requests to protected endpoints return 403 Forbidden
- Invalid data submissions return 400 Bad Request with field-specific error messages
- Deleted resources return 204 No Content on success