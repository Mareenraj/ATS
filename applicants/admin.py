"""
Admin configuration for applicants.
"""
from django.contrib import admin
from .models import Applicant, ApplicantNote


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    """Admin interface for Applicant model."""
    list_display = ['full_name', 'email', 'applied_job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['first_name', 'last_name', 'email']
    date_hierarchy = 'applied_at'


@admin.register(ApplicantNote)
class ApplicantNoteAdmin(admin.ModelAdmin):
    """Admin interface for ApplicantNote model."""
    list_display = ['applicant', 'created_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['note', 'applicant__first_name', 'applicant__last_name']