# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (register, user_login, user_logout,delete_profile,
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
                    pharmacy
                    )


app_name = 'accountsHSM'

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('delete_profile/', delete_profile, name='delete_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
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
    path('provider/profile/create/', create_provider_profile, name='create_provider_profile'),  #
]