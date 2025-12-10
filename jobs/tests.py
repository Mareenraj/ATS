"""
Tests for jobs app.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import Job


class JobModelTestCase(TestCase):
    """Test cases for Job model."""

    def setUp(self):
        self.user = User.objects.create_user(username='recruiter', password='pass123')
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Test description',
            location='Remote',
            employment_type='FT',
            requirements='Python, Django',
            responsibilities='Build applications',
            deadline=date.today() + timedelta(days=30),
            created_by=self.user
        )

    def test_job_creation(self):
        """Test job is created correctly."""
        self.assertEqual(self.job.title, 'Software Engineer')
        self.assertFalse(self.job.is_expired)

    def test_job_str(self):
        """Test job string representation."""
        self.assertEqual(str(self.job), 'Software Engineer - Remote')


class JobViewTestCase(TestCase):
    """Test cases for job views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='recruiter', password='pass123')
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Test description',
            location='Remote',
            employment_type='FT',
            requirements='Python',
            responsibilities='Code',
            deadline=date.today() + timedelta(days=30),
            created_by=self.user
        )

    def test_job_list_view(self):
        """Test job list view."""
        response = self.client.get(reverse('jobs:job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Engineer')

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication."""
        response = self.client.get(reverse('jobs:dashboard'))
        self.assertEqual(response.status_code, 302) 