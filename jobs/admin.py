"""
Admin configuration for jobs.
"""
from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Admin interface for Job model."""
    list_display = ['title', 'location', 'employment_type', 'created_by', 'deadline', 'is_active']
    list_filter = ['employment_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'created_at'
