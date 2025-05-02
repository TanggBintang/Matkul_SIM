# seminar/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('registration/<int:seminar_id>/', views.seminar_registration, name='seminar_registration'),
]