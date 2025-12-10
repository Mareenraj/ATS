"""
Views for job management and dashboard.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import Job
from .forms import JobForm
from applicants.models import Applicant


def job_list_view(request):
    """Public view of all active job postings."""
    jobs = Job.objects.filter(is_active=True).annotate(
        applicant_count=Count('applicants')
    )
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


def job_detail_view(request, pk):
    """Public view of job details."""
    job = get_object_or_404(Job, pk=pk, is_active=True)
    return render(request, 'jobs/job_detail.html', {'job': job})


@login_required
def dashboard_view(request):
    """Recruiter dashboard showing jobs and recent applicants."""
    jobs = Job.objects.filter(created_by=request.user).annotate(
        applicant_count=Count('applicants')
    )
    recent_applicants = Applicant.objects.filter(
        applied_job__created_by=request.user
    ).order_by('-applied_at')[:10]

    # Statistics
    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    total_applicants = Applicant.objects.filter(applied_job__created_by=request.user).count()

    context = {
        'jobs': jobs,
        'recent_applicants': recent_applicants,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applicants': total_applicants,
    }
    return render(request, 'jobs/dashboard.html', context)


@login_required
def job_create_view(request):
    """View for creating new job posting."""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('jobs:dashboard')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Create Job Posting'})


@login_required
def job_edit_view(request, pk):
    """View for editing job posting."""
    job = get_object_or_404(Job, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('jobs:dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Edit Job Posting', 'job': job})


@login_required
def job_delete_view(request, pk):
    """View for deleting job posting."""
    job = get_object_or_404(Job, pk=pk, created_by=request.user)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully!')
        return redirect('jobs:dashboard')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})