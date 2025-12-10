"""
Job posting models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Job(models.Model):
    """Model representing a job posting."""

    EMPLOYMENT_TYPES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('IN', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=2, choices=EMPLOYMENT_TYPES, default='FT')
    salary_range = models.CharField(max_length=100, blank=True)
    requirements = models.TextField(help_text='Job requirements and qualifications')
    responsibilities = models.TextField(help_text='Key responsibilities')
    deadline = models.DateField(help_text='Application deadline')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"

    @property
    def is_expired(self):
        """Check if job posting has expired."""
        return timezone.now().date() > self.deadline

    @property
    def application_count(self):
        """Get total number of applications."""
        return self.applicants.count()
