from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Patient, AdministrativeStaff, HealthcareProvider, Appointment, Prescription, Invoices

# UserCreationForm is built-in Django form that handles the creation of new users.
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        # Meta: Links this form to the User model and specifies the fields to include in the form.
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

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
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'provider': forms.Select(attrs={'class': 'form-control'}),
        } # When a field is disabled, users can see the field and its value, but they cannot interact with it.

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'provider', 'medication', 'dosage', 'instructions' , 'service_description']


class InvoicesForm(forms.ModelForm):
    class Meta:
        model = Invoices
        fields = ['prescription','date','total_amount','Insurance_percent_cover' , 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }