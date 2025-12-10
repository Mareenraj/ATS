"""
Forms for applicant management.
"""
from django import forms
from .models import Applicant, ApplicantNote


class ApplicationForm(forms.ModelForm):
    """Form for job application submission."""

    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'email', 'phone', 'linkedin', 'resume', 'cover_letter']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'linkedin': forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'LinkedIn Profile URL (optional)'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Cover Letter (optional)'}),
        }


class ApplicantStatusForm(forms.ModelForm):
    """Form for updating applicant status."""

    class Meta:
        model = Applicant
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class ApplicantNoteForm(forms.ModelForm):
    """Form for adding notes to applicants."""

    class Meta:
        model = ApplicantNote
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a note...'}),
        }