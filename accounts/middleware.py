# myapp/middleware.py

from django.shortcuts import redirect
from django.urls import resolve, Resolver404

class RedirectInvalidUrlsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of valid URLs
        valid_urls = valid_urls = [
            'register', 'login', 'logout', 'delete_profile',
            'password_reset', 'password_reset_done',
            'password_reset_confirm', 'password_reset_complete',
            'schedule_appointment', 'patient_dashboard',
            'appointments_list_admin', 'appointments_list_provider',
            'prescription_view', 'edit_prescription',
            'delete_prescription', 'add_prescription',
            'pharmacy', 'download_invoice', 'invoice_view',
            'add_invoice', 'edit_invoice', 'invoice_detail',
            'invoice_pay', 'delete_invoice', 'patients_insurance',
            'service_description', 'reporting_dashboard',
            'download_report_summary', 'download_report_detail',
            'patient_profile', 'admin_profile', 'provider_profile',
            'create_patient_profile', 'create_admin_profile',
            'create_provider_profile','download_revenue','admin'
        ]


        try:
            # Check if the requested URL is valid
            resolved_url = resolve(request.path)
            if resolved_url.url_name not in valid_urls:
                return redirect('accounts:login')  # Redirect to the login page
        except Resolver404:
            return redirect('accounts:login')  # Redirect if URL is not found

        response = self.get_response(request)
        return response