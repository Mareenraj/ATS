"""
Forms for job management.
"""
from django import forms
from .models import Job


class JobForm(forms.ModelForm):
    """Form for creating and editing job postings."""

    class Meta:
        model = Job
        fields = [
            'title', 'description', 'location', 'employment_type',
            'salary_range', 'requirements', 'responsibilities', 'deadline', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., LKR 160,000 - LKR 200,000'}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }