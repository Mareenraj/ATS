"""
Applicant tracking models.
"""
from django.db import models
from jobs.models import Job


class Applicant(models.Model):
    """Model representing a job applicant."""

    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]

    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    linkedin = models.URLField(blank=True, null=True)

    # Application details
    applied_job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')

    # Metadata
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-applied_at']
        unique_together = [
            ['applied_job', 'email'],
            ['applied_job', 'phone']
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.applied_job.title}"

    @property
    def full_name(self):
        """Return full name of applicant."""
        return f"{self.first_name} {self.last_name}"


class ApplicantNote(models.Model):
    """Model for recruiter notes on applicants."""

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.applicant.full_name} by {self.created_by.username}"



