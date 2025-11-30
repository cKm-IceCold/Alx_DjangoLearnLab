"""
Unit tests for Book API endpoints.
Covers: list/detail/create/update/delete, plus filtering, search and ordering,
and permission enforcement (authenticated vs admin).
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Book, Author

User = get_user_model()

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Users
        self.user_password = "testpass"
        self.staff_password = "staffpass"
        self.user = User.objects.create_user(username="tester", password=self.user_password)
        self.staff = User.objects.create_user(username="staff", password=self.staff_password, is_staff=True)

        # Authors
        self.author1 = Author.objects.create(name="Alice")
        self.author2 = Author.objects.create(name="Bob")

        # Books
        self.book1 = Book.objects.create(title="Django Basics", author=self.author1, publication_year=2021)
        self.book2 = Book.objects.create(title="Advanced Python", author=self.author2, publication_year=2023)
        self.book3 = Book.objects.create(title="Python Patterns", author=self.author2, publication_year=2022)

        self.client = APIClient()

    # List / filtering / search / ordering
    def test_list_filter_by_publication_year(self):
        response = self.client.get("/api/books/?publication_year=2023")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data  # use DRF Response.data
        # Only book2 has 2023
        self.assertTrue(any(b["id"] == self.book2.id for b in data))
        self.assertFalse(any(b["id"] == self.book1.id for b in data))

    def test_search_by_title_or_author(self):
        response = self.client.get("/api/books/?search=Python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [b["id"] for b in response.data]  # use response.data
        self.assertIn(self.book2.id, ids)
        self.assertIn(self.book3.id, ids)
        self.assertNotIn(self.book1.id, ids)

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get("/api/books/?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        years = [b["publication_year"] for b in data]
        self.assertEqual(years, sorted(years, reverse=True))

    def test_retrieve_book_detail(self):
        response = self.client.get(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # check response payload via response.data
        self.assertEqual(response.data.get("title"), self.book1.title)

    def test_create_requires_authentication(self):
        payload = {"title": "New Book", "author": self.author1.id, "publication_year": 2020}
        response = self.client.post("/api/books/create/", payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated user can create (use client.login)
        self.client.login(username=self.user.username, password=self.user_password)
        response2 = self.client.post("/api/books/create/", payload, format="json")
        # assert status and returned data fields
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response2.data)
        self.assertEqual(response2.data.get("title"), payload["title"])
        self.assertTrue(Book.objects.filter(title="New Book").exists())
        self.client.logout()

    def test_update_requires_authentication(self):
        update_payload = {"title": "Django Basics Updated"}
        # unauthenticated
        response = self.client.patch(f"/api/books/update/{self.book1.id}/", update_payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # authenticated (use client.login)
        self.client.login(username=self.user.username, password=self.user_password)
        response2 = self.client.patch(f"/api/books/update/{self.book1.id}/", update_payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        # validate changed data returned by API
        self.assertEqual(response2.data.get("title"), "Django Basics Updated")
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Django Basics Updated")
        self.client.logout()

    def test_delete_requires_admin(self):
        # non-admin attempt (use client.login)
        self.client.login(username=self.user.username, password=self.user_password)
        response = self.client.delete(f"/api/books/delete/{self.book2.id}/")
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertTrue(Book.objects.filter(id=self.book2.id).exists())
        self.client.logout()

        # admin/staff can delete (use client.login)
        self.client.login(username=self.staff.username, password=self.staff_password)
        response2 = self.client.delete(f"/api/books/delete/{self.book2.id}/")
        self.assertIn(response2.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        # DB assertion is the authoritative check
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())
        self.client.logout()