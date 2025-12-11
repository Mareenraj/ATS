"""
Views for applicant management.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobs.models import Job
from .models import Applicant, ApplicantNote
from .forms import ApplicationForm, ApplicantStatusForm, ApplicantNoteForm
from .utils import extract_text_from_pdf, analyze_cv_with_gemini


def apply_view(request, job_id):
    """View for job application submission."""
    job = get_object_or_404(Job, pk=job_id, is_active=True)

    # Prevent job owner from applying to their own job
    if request.user.is_authenticated and request.user == job.created_by:
        messages.error(request, 'You cannot apply to your own job posting.')
        return redirect('jobs:job_detail', pk=job_id)

    if job.is_expired:
        messages.error(request, 'This job posting has expired.')
        return redirect('jobs:job_detail', pk=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.applied_job = job
            applicant.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('applicants:application_success')
    else:
        form = ApplicationForm()

    return render(request, 'applicants/apply.html', {'form': form, 'job': job})


def application_success_view(request):
    """View shown after successful application."""
    return render(request, 'applicants/success.html')


@login_required
def applicant_list_view(request):
    """View listing all applicants for recruiter's jobs."""
    job_id = request.GET.get('job')
    status = request.GET.get('status')

    applicants = Applicant.objects.filter(applied_job__created_by=request.user)

    if job_id:
        applicants = applicants.filter(applied_job_id=job_id)
    if status:
        applicants = applicants.filter(status=status)

    jobs = Job.objects.filter(created_by=request.user)

    context = {
        'applicants': applicants,
        'jobs': jobs,
        'selected_job': job_id,
        'selected_status': status,
        'status_choices': Applicant.STATUS_CHOICES,
    }
    return render(request, 'applicants/applicant_list.html', context)


@login_required
def applicant_detail_view(request, pk):
    """View showing applicant details with resume preview."""
    applicant = get_object_or_404(
        Applicant,
        pk=pk,
        applied_job__created_by=request.user
    )

    # Handle status update
    if request.method == 'POST' and 'update_status' in request.POST:
        status_form = ApplicantStatusForm(request.POST, instance=applicant)
        if status_form.is_valid():
            status_form.save()
            messages.success(request, 'Status updated successfully!')
            return redirect('applicants:applicant_detail', pk=pk)

    # Handle note addition
    if request.method == 'POST' and 'add_note' in request.POST:
        note_form = ApplicantNoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.applicant = applicant
            note.created_by = request.user
            note.save()
            messages.success(request, 'Note added successfully!')
            return redirect('applicants:applicant_detail', pk=pk)

    # Extract resume text if PDF
    resume_text = None
    ai_analysis = None
    if applicant.resume and applicant.resume.name.endswith('.pdf'):
        resume_text = extract_text_from_pdf(applicant.resume.path)

    # AI Analysis - only run when requested via button click
    if request.method == 'POST' and 'analyze_cv' in request.POST:
        if resume_text and not resume_text.startswith("Error") and not resume_text.startswith("Unable"):
            job = applicant.applied_job
            ai_analysis = analyze_cv_with_gemini(
                resume_text=resume_text,
                job_description=job.description,
                job_title=job.title,
                job_requirements=job.requirements
            )
            if ai_analysis.get('error'):
                messages.warning(request, f"AI Analysis: {ai_analysis['error']}")
        else:
            messages.warning(request, "Cannot analyze - resume text extraction failed.")

    status_form = ApplicantStatusForm(instance=applicant)
    note_form = ApplicantNoteForm()
    notes = applicant.notes.all()

    context = {
        'applicant': applicant,
        'status_form': status_form,
        'note_form': note_form,
        'notes': notes,
        'resume_text': resume_text,
        'ai_analysis': ai_analysis,
    }
    return render(request, 'applicants/applicant_detail.html', context)


@login_required
def applicant_delete_view(request, pk):
    """View for deleting an applicant."""
    applicant = get_object_or_404(
        Applicant,
        pk=pk,
        applied_job__created_by=request.user
    )

    if request.method == 'POST':
        applicant_name = applicant.full_name
        applicant.delete()
        messages.success(request, f'Applicant "{applicant_name}" has been deleted.')
        return redirect('applicants:applicant_list')

    return render(request, 'applicants/applicant_confirm_delete.html', {'applicant': applicant})
