from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='pass123'
        )

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/posts/', {
            'title': 'Test',
            'content': 'Testing'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
