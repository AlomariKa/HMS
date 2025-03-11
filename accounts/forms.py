from datetime import date, time, timedelta, datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'provider': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Always set the time field as a Select widget with empty choices initially
        self.fields['time'].widget = forms.Select(choices=[])

        # If a date is provided, update the choices
        if 'initial' in kwargs and 'date' in kwargs['initial']:
            appointment_date = kwargs['initial']['date']
            available_slots = generate_available_time_slots(appointment_date)
            formatted_slots = [(slot, slot.strftime('%H:%M')) for slot in available_slots]
            self.fields['time'].widget.choices = formatted_slots

        self.fields['date'].widget.attrs['min'] = date.today().isoformat()

    def clean(self):
        cleaned_data = super().clean()
        appointment_date = cleaned_data.get('date')
        appointment_time = cleaned_data.get('time')

        if appointment_date:
            if appointment_date < date.today():
                raise ValidationError("Appointments cannot be scheduled for past dates.")
            if appointment_date.weekday() >= 5:
                raise ValidationError("Appointments can only be scheduled from Monday to Friday.")

        if appointment_time:
            if appointment_time < time(8, 0) or appointment_time >= time(16, 0):
                raise ValidationError("Appointments can only be scheduled between 8 AM and 4 PM.")
            if appointment_time.minute % 30 != 0:
                raise ValidationError("Appointments must be scheduled at 30-minute intervals.")

        return cleaned_data


def generate_available_time_slots(appointment_date):
    """Generate available time slots for a given appointment date."""

    if not appointment_date or appointment_date < date.today():
        return []  # Don't allow past dates

    start_time = time(8, 0)
    end_time = time(16, 0)

    # Only apply the time restriction if the selected date is today
    if appointment_date == date.today():
        now = datetime.now().time()
        if now.minute % 30 != 0:
            now = (datetime.combine(date.today(), now) + timedelta(minutes=(30 - now.minute))).time()
        start_time = max(start_time, now)

    time_slots = []
    current_time = datetime.combine(appointment_date, start_time)

    while current_time.time() < end_time:
        # Truncate microseconds
        time_slots.append(current_time.time().replace(microsecond=0))
        current_time += timedelta(minutes=30)

    # Corrected occupied_slots query
    occupied_slots = Appointment.objects.filter(
        date=appointment_date
    ).values_list('time', flat=True)

    available_slots = [slot for slot in time_slots if slot not in occupied_slots]

    # Calculate the next hour
    next_hour = (datetime.now() + timedelta(hours=1)).time()

    # Exclude time slots within the next hour
    available_slots = [
        slot for slot in available_slots
        if slot > next_hour or appointment_date > date.today()  # Allow slots for future dates
    ]
    return available_slots
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