"""
URL patterns for applicants app.
"""
from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_view, name='apply'),
    path('success/', views.application_success_view, name='application_success'),
    path('list/', views.applicant_list_view, name='applicant_list'),
    path('<int:pk>/', views.applicant_detail_view, name='applicant_detail'),
    path('<int:pk>/delete/', views.applicant_delete_view, name='applicant_delete'),
]