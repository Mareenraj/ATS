"""
Management command to load sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from datetime import date, timedelta
from jobs.models import Job
from applicants.models import Applicant


class Command(BaseCommand):
    help = 'Load sample jobs and applicants for testing'

    def handle(self, *args, **kwargs):
        # Create sample recruiter
        recruiter, created = User.objects.get_or_create(
            username='recruiter',
            defaults={
                'email': 'recruiter@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith'
            }
        )
        if created:
            recruiter.set_password('recruiter123')
            recruiter.save()
            self.stdout.write(self.style.SUCCESS('Created recruiter user'))

        # Create sample jobs
        sample_jobs = [
            {
                'title': 'Senior Python Developer',
                'description': 'We are seeking an experienced Python developer...',
                'location': 'Remote',
                'employment_type': 'FT',
                'salary_range': '$100,000 - $130,000',
                'requirements': 'Python, Django, PostgreSQL, 5+ years experience',
                'responsibilities': 'Design and implement backend services, mentor junior developers',
            },
            {
                'title': 'Frontend Engineer',
                'description': 'Join our team to build amazing user interfaces...',
                'location': 'San Francisco, CA',
                'employment_type': 'FT',
                'salary_range': '$90,000 - $120,000',
                'requirements': 'JavaScript, React, CSS, 3+ years experience',
                'responsibilities': 'Build responsive web applications, collaborate with designers',
            },
            {
                'title': 'DevOps Engineer',
                'description': 'Help us scale our infrastructure...',
                'location': 'New York, NY',
                'employment_type': 'FT',
                'salary_range': '$110,000 - $140,000',
                'requirements': 'AWS, Docker, Kubernetes, CI/CD, 4+ years experience',
                'responsibilities': 'Manage cloud infrastructure, automate deployments',
            },
            {
                'title': 'Data Scientist Intern',
                'description': 'Summer internship opportunity for data science students...',
                'location': 'Boston, MA',
                'employment_type': 'IN',
                'salary_range': '$25/hour',
                'requirements': 'Python, SQL, Machine Learning, Currently enrolled in university',
                'responsibilities': 'Analyze data, build ML models, present findings',
            },
            {
                'title': 'Product Manager',
                'description': 'Lead product development for our flagship application...',
                'location': 'Austin, TX',
                'employment_type': 'FT',
                'salary_range': '$120,000 - $150,000',
                'requirements': 'Product management experience, Technical background, 5+ years',
                'responsibilities': 'Define product roadmap, work with engineering and design teams',
            },
        ]

        jobs = []
        for job_data in sample_jobs:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                created_by=recruiter,
                defaults={
                    **job_data,
                    'deadline': date.today() + timedelta(days=60)
                }
            )
            jobs.append(job)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created job: {job.title}'))

        # Create sample applicants
        sample_applicants = [
            {
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'email': 'alice@example.com',
                'phone': '555-0101',
                'linkedin': 'https://linkedin.com/in/alicejohnson',
                'status': 'screening',
            },
            {
                'first_name': 'Bob',
                'last_name': 'Williams',
                'email': 'bob@example.com',
                'phone': '555-0102',
                'linkedin': 'https://linkedin.com/in/bobwilliams',
                'status': 'interview',
            },
            {
                'first_name': 'Charlie',
                'last_name': 'Brown',
                'email': 'charlie@example.com',
                'phone': '555-0103',
                'status': 'applied',
            },
        ]

        # Create dummy PDF content
        dummy_resume = ContentFile(b'%PDF-1.4\nDummy Resume Content', name='resume.pdf')

        for i, applicant_data in enumerate(sample_applicants):
            job = jobs[i % len(jobs)]  # Distribute applicants across jobs
            applicant, created = Applicant.objects.get_or_create(
                email=applicant_data['email'],
                applied_job=job,
                defaults={
                    **applicant_data,
                    'resume': dummy_resume,
                    'cover_letter': f'I am very interested in the {job.title} position...'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Created applicant: {applicant.full_name} for {job.title}'
                ))

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write(f'Login with: username=recruiter, password=recruiter123')