"""
URL patterns for accounts app.
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.RecruiterLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]