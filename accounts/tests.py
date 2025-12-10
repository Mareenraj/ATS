"""
Tests for accounts app.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class AccountsTestCase(TestCase):
    """Test cases for authentication."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_login_view(self):
        """Test login page loads."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        """Test user can login."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_register_view(self):
        """Test registration page loads."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
