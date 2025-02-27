
from django import forms
from .models import Patient, AdministrativeStaff, HealthcareProvider, Appointment

class PatientForm(forms.ModelForm):
    class Meta: # help give me information and specify things
        model = Patient
        fields = ['name', 'age', 'medical_history', 'allergies', 'insurance_detail']

class AdministrativeStaffForm(forms.ModelForm):
    class Meta:
        model = AdministrativeStaff
        fields = ['name', 'contact_number']

class HealthcareProviderForm(forms.ModelForm):
    class Meta:
        model = HealthcareProvider
        fields = ['name', 'specialization', 'contact_number']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['provider', 'date', 'time']
        widgets = { # using Widgets HTML attributes to customize the appearance and behavior of the form fields.
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'disabled': 'disabled'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'disabled': 'disabled'}),
            'provider': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
        } # When a field is disabled, users can see the field and its value, but they cannot interact with it.