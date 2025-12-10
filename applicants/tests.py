"""
Tests for applicants app.
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from jobs.models import Job
from .models import Applicant


class ApplicantModelTestCase(TestCase):
    """Test cases for Applicant model."""

    def setUp(self):
        self.user = User.objects.create_user(username='recruiter', password='pass123')
        self.job = Job.objects.create(
            title='Software Engineer',
            description='Test',
            location='Remote',
            employment_type='FT',
            requirements='Python',
            responsibilities='Code',
            deadline=date.today() + timedelta(days=30),
            created_by=self.user
        )
        self.applicant = Applicant.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            applied_job=self.job,
            resume=SimpleUploadedFile('resume.pdf', b'file content')
        )

    def test_applicant_creation(self):
        """Test applicant is created correctly."""
        self.assertEqual(self.applicant.full_name, 'John Doe')
        self.assertEqual(self.applicant.status, 'applied')

    def test_applicant_str(self):
        """Test applicant string representation."""
        expected = 'John Doe - Software Engineer'
        self.assertEqual(str(self.applicant), expected)
