# Classes/urls.py

from django.urls import path
from .views import (
    schedule_appointment,
 patient_dashboard,
 appointments_list_admin,
appointments_list_provider,
 create_admin_profile,
 create_patient_profile,
 create_provider_profile,
 patient_profile,
 provider_profile,
 admin_profile,
prescription_view,
edit_prescription,
delete_prescription,
add_prescription,
pharmacy)

app_name = 'logicHSM'

urlpatterns = [
    path('appointments/schedule/', schedule_appointment, name='schedule_appointment'),
    path('appointments/patient_dashboard/', patient_dashboard, name='patient_dashboard'),
    path('appointments/listAdmin/', appointments_list_admin, name='appointments_list_admin'),
    path('appointments/listProvider/', appointments_list_provider, name='appointments_list_provider'),

    path('prescriptions/', prescription_view, name='prescription_view'),
    path('prescriptions/edit/<int:prescription_id>/', edit_prescription, name='edit_prescription'),
    path('prescriptions/delete/<int:prescription_id>/', delete_prescription, name='delete_prescription'),
    path('prescriptions/add/', add_prescription, name='add_prescription'),  # Add a new prescription
    path('pharmacy/',pharmacy,name='pharmacy'),

    path('patient_profile/', patient_profile, name='patient_profile'),  # Patient dashboard
    path('admin_profile/', admin_profile, name='admin_profile'),  # Admin dashboard
    path('provider_profile/', provider_profile, name='provider_profile'),  # Provider dashboard

    path('patient/profile/create/', create_patient_profile, name='create_patient_profile'),  # New URL
    path('administrativestaff/profile/create/', create_admin_profile, name='create_admin_profile'),  # New URL
    path('provider/profile/create/', create_provider_profile, name='create_provider_profile'),  # New URL
]