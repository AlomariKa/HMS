# Classes/views.py

from django.shortcuts import render, redirect , get_object_or_404
from .forms import PatientForm, AdministrativeStaffForm, HealthcareProviderForm,AppointmentForm
from .models import Appointment,Patient, AdministrativeStaff,HealthcareProvider
from django.contrib.auth.decorators import login_required
from django.urls import reverse





@login_required # ensures that only authenticated users can acces
def patient_profile(request):
    try:
        user_profile = request.user.userprofile  # Access the UserProfile
        patient = user_profile.patient
    except Patient.DoesNotExist:
        # Redirect to profile creation page if the user does not have a Patient profile
        return redirect('logic:create_patient_profile')  # You need to create this view

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        # Without instance=patient, the form would create a new patient.
        # With instance=patient, the form updates the existing patient you already have.
        if form.is_valid():
            form.save()

            return redirect('logic:patient_profile')  # Redirect to the same page to see updated info
    else:
        form = PatientForm(instance=patient)

    return render(request, 'Profiles/patient_profile.html', {'form': form})


def create_patient_profile(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False) # save the form data to a Patient object without committing it to the database immediately.
            patient.user_profile = request.user.userprofile  # Link to the user profile
            patient.save()
            return redirect('logic:patient_profile')  # Redirect to the patient profile
    else:
        form = PatientForm()

    return render(request, 'CreateProfiles/create_patient_profile.html', {'form': form})



@login_required
def admin_profile(request):
    try:
        user_profile = request.user.userprofile  # Access the UserProfile
        admin = user_profile.administrativestaff    # Assuming the user has an Admin profile
    except AdministrativeStaff.DoesNotExist:
        return redirect('logic:create_admin_profile')  # You need to create this view
    if request.method == 'POST':
        form = AdministrativeStaffForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('logic:admin_profile')  # Redirect to the same page to see updated info
    else:
        form = AdministrativeStaffForm(instance=admin)

    return render(request, 'Profiles/admin_profile.html', {'form': form})

def create_admin_profile(request):
    if request.method == 'POST':
        form = AdministrativeStaffForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.user_profile = request.user.userprofile  # Link to the user profile
            admin.save()
            return redirect('logic:admin_profile')  # Redirect to the admin profile
    else:
        form = AdministrativeStaffForm()

    return render(request, 'CreateProfiles/create_admin_profile.html', {'form': form})

@login_required
def provider_profile(request):
    try:
        user_profile = request.user.userprofile
        provider = user_profile.healthcareprovider  # Access the Provider through UserProfile
    except HealthcareProvider.DoesNotExist:
        return redirect('logic:create_provider_profile')  # You need to create this view

    if request.method == 'POST':
        form = HealthcareProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('logic:provider_profile')  # Redirect to the same page to see updated info
    else:
        form = HealthcareProviderForm(instance=provider)

    return render(request, 'Profiles/provider_profile.html', {'form': form})


def create_provider_profile(request):
    if request.method == 'POST':
        form = HealthcareProviderForm(request.POST)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.user_profile = request.user.userprofile  # Link to the user profile
            provider.save()
            return redirect('logic:provider_profile')  # Redirect to the provider profile
    else:
        form = HealthcareProviderForm()

    return render(request, 'CreateProfiles/create_provider_profile.html', {'form': form})

def schedule_appointment(request):
    try:
        user_profile = request.user.userprofile  # Access the UserProfile
        patient = user_profile.patient  # Access the Patient through UserProfile
    except Patient.DoesNotExist:
        return redirect('create_patient_profile')  # Redirect to profile creation if not found
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient  # This links the appointment to the specific patient.
            appointment.save()
            return redirect('logic:patient_dashboard')  # Redirect to view upcoming appointments
    else:
        form = AppointmentForm()

    return render(request, 'appointments/schedule_appointment.html', {'form': form})

@login_required
def patient_dashboard(request):
    try:
        user_profile = request.user.userprofile
        patient = user_profile.patient  # Access the Patient through UserProfile
        appointments = patient.appointment_set.all()  # because of foreign key Django provides a way to access all related Appointment objects through the patient instance.
    except Patient.DoesNotExist:
        return redirect('logic:create_patient_profile')  # Redirect to profile creation if not found
    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments})

def appointments_list_admin(request):
    # Retrieve all appointments
    appointments = Appointment.objects.all()
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()
        return redirect('logic:appointments_list_admin')
    return render(request, 'appointments/appointments_list_admin.html', {'appointments': appointments})

def appointments_list_provider(request):
    # Retrieve all appointments
    appointments = Appointment.objects.all()

    return render(request, 'appointments/appointments_list_provider.html', {'appointments': appointments})