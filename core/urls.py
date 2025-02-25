from django.urls import path
from . import views

urlpatterns = [
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('schedule-appointment/', views.schedule_appointment, name='schedule_appointment'),
]