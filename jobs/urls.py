"""
URL patterns for jobs app.
"""
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list_view, name='job_list'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/', views.job_create_view, name='job_create'),
    path('<int:pk>/edit/', views.job_edit_view, name='job_edit'),
    path('<int:pk>/delete/', views.job_delete_view, name='job_delete'),
]