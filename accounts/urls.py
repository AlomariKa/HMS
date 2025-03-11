# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (register, user_login, user_logout, delete_profile,
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
                    pharmacy,
                    invoice_view,
                    edit_invoice,
                    invoice_detail,
                    invoice_pay, add_invoice, delete_invoice, patients_insurance, service_description,
                    reporting_dashboard, download_report_summary, download_report_detail, download_invoice, download_revenue,
                    receive_device_data, device_data_view
                    )



app_name = 'accountsHSM'

urlpatterns = [
    # Authentication
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('delete_profile/', delete_profile, name='delete_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Appointments
    path('appointments/schedule/', schedule_appointment, name='schedule_appointment'),
    path('appointments/patient_dashboard/', patient_dashboard, name='patient_dashboard'),
    path('appointments/listAdmin/', appointments_list_admin, name='appointments_list_admin'),
    path('appointments/listProvider/', appointments_list_provider, name='appointments_list_provider'),

    #Prescriptions
    path('prescriptions/', prescription_view, name='prescription_view'),
    path('prescriptions/edit/<int:prescription_id>/', edit_prescription, name='edit_prescription'),
    path('prescriptions/delete/<int:prescription_id>/', delete_prescription, name='delete_prescription'),
    path('prescriptions/add/', add_prescription, name='add_prescription'),
    path('pharmacy/<int:prescription_id>/',pharmacy,name='pharmacy'),

    #Invoices
    path('invoice/download/<int:invoice_id>/', download_invoice, name='download_invoice'),
    path('invoices/', invoice_view , name='invoice_view'),
    path('invoice/add',add_invoice,name='add_invoice'),
    path('invoice/edit/<int:invoice_id>', edit_invoice, name='edit_invoice'),
    path('invoice/detail/<int:invoice_id>',invoice_detail,name='invoice_detail'),
    path('invoice/pay/<int:invoice_id>',invoice_pay,name='invoice_pay'),
    path('invoice/delete/<int:invoice_id>/', delete_invoice, name='delete_invoice'),
    path('patients/insurance/',patients_insurance,name='patients_insurance'),
    path('Prescriptions/service/', service_description, name='service_description'),

    #Reporting
    path('reporting/dashboard/', reporting_dashboard, name='reporting_dashboard'),
    path('reporting/download/summary', download_report_summary, name='download_report_summary'),
    path('reporting/download/detail', download_report_detail, name='download_report_detail'),
    path('reporting/download/revenue',download_revenue, name='download_revenue'),

    #Ptofiles
    path('patient_profile/', patient_profile, name='patient_profile'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('provider_profile/', provider_profile, name='provider_profile'),

    # Create Data for Profile
    path('patient/profile/create/', create_patient_profile, name='create_patient_profile'),
    path('administrativestaff/profile/create/', create_admin_profile, name='create_admin_profile'),
    path('provider/profile/create/', create_provider_profile, name='create_provider_profile'),

    #Device
    path('device-data/', receive_device_data, name='receive_device_data'),
    path('device-data-view/', device_data_view, name='device_data_view'),  # New URL

]