
from django import forms
from .models import Patient, AdministrativeStaff, HealthcareProvider, Appointment

class PatientForm(forms.ModelForm):
    class Meta:
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
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'disabled': 'disabled'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'disabled': 'disabled'}),
            'provider': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),  # Initially disabled
        }