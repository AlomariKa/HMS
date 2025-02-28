# accounts/views.py
from django.contrib.auth import login, authenticate, logout # These functions are used for handling user authentication, logging users in and out.
from django.contrib import messages # This module is used to display messages to users.
from django.shortcuts import render, redirect , get_object_or_404
from .forms import PatientForm, AdministrativeStaffForm, HealthcareProviderForm,AppointmentForm,PrescriptionForm,UserRegisterForm
from .models import UserProfile,Appointment,Patient, AdministrativeStaff,HealthcareProvider,Prescription
from django.contrib.auth.decorators import login_required
from .decorators import provider_required,admin_required,patient_required, new_provider_required,new_admin_required,new_patient_required

# User Authentication #
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type') # Retrieves the user_type from the form.
            user.userprofile.user_type = user_type # Sets the user_type in the user profile.
            user.userprofile.save() # It helps create a more secure and user-friendly application.
            login(request, user)  # Automatically log in the user after registration
            messages.success(request, 'Registration successful.')
            return redirect('accounts:login')  # Redirect to a home page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.userprofile.user_type
            if user_type == 'patient':
                return redirect('accounts:patient_profile')
            elif user_type == 'admin':
                return redirect('accounts:admin_profile')
            elif user_type == 'provider':
                return redirect('accounts:provider_profile')
            messages.success(request, 'Login successful.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')  # Redirect to login page

@login_required
def delete_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':

        # Delete the user profile
        user_profile.delete()
        # Optionally, delete the user account if needed
        request.user.delete()  # Uncomment if you want to delete the user account as well

        # Log the user out
        logout(request)
        return redirect('accounts:login')  # Redirect to the login page

    return render(request, 'delete_profile/delete_profile.html', {'user_profile': request.user})



@login_required # ensures that only authenticated users can acces
def patient_profile(request):
    try:
        user_profile = request.user.userprofile  # Access the UserProfile
        patient = user_profile.patient

    except Patient.DoesNotExist:
        # Redirect to profile creation page if the user does not have a Patient profile
        return redirect('accounts:create_patient_profile')  # You need to create this view

    if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'patient'):
        return redirect('accounts:login')

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        # Without instance=patient, the form would create a new patient.
        # With instance=patient, the form updates the existing patient you already have.
        if form.is_valid():
            form.save()

            return redirect('accounts:patient_profile')  # Redirect to the same page to see updated info
    else:
        form = PatientForm(instance=patient)

    return render(request, 'Profiles/patient_profile.html', {'form': form})

@new_patient_required
@login_required
def create_patient_profile(request):

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False) # save the form data to a Patient object without committing it to the database immediately.
            patient.user_profile = request.user.userprofile  # Link to the user profile
            patient.save()
            return redirect('accounts:patient_profile')  # Redirect to the patient profile
    else:
        form = PatientForm()

    return render(request, 'CreateProfiles/create_patient_profile.html', {'form': form})



@login_required
def admin_profile(request):
    try:
        user_profile = request.user.userprofile
        admin = user_profile.administrativestaff
    except AdministrativeStaff.DoesNotExist:
        return redirect('accounts:create_admin_profile')

    if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'administrativestaff'):
        return redirect('accounts:login')

    if request.method == 'POST':
        form = AdministrativeStaffForm(request.POST, instance=admin)
        if form.is_valid():
            form.save()
            return redirect('accounts:admin_profile')  # Redirect to the same page to see updated info
    else:
        form = AdministrativeStaffForm(instance=admin)

    return render(request, 'Profiles/admin_profile.html', {'form': form})

@new_admin_required
@login_required
def create_admin_profile(request):

    if request.method == 'POST':
        form = AdministrativeStaffForm(request.POST)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.user_profile = request.user.userprofile  # Link to the user profile
            admin.save()
            return redirect('accounts:admin_profile')  # Redirect to the admin profile
    else:
        form = AdministrativeStaffForm()

    return render(request, 'CreateProfiles/create_admin_profile.html', {'form': form})


@login_required
def provider_profile(request):
    try:
        user_profile = request.user.userprofile
        provider = user_profile.healthcareprovider  # Access the Provider through UserProfile
    except HealthcareProvider.DoesNotExist:
        return redirect('accounts:create_provider_profile')  # You need to create this view

    if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'healthcareprovider'):
        return redirect('accounts:login')
    if request.method == 'POST':
        form = HealthcareProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('accounts:provider_profile')  # Redirect to the same page to see updated info
    else:
        form = HealthcareProviderForm(instance=provider)

    return render(request, 'Profiles/provider_profile.html', {'form': form})

@new_provider_required
@login_required
def create_provider_profile(request):

    if request.method == 'POST':
        form = HealthcareProviderForm(request.POST)
        if form.is_valid():
            provider = form.save(commit=False)
            provider.user_profile = request.user.userprofile  # Link to the user profile
            provider.save()
            return redirect('accounts:provider_profile')  # Redirect to the provider profile
    else:
        form = HealthcareProviderForm()

    return render(request, 'CreateProfiles/create_provider_profile.html', {'form': form})

@patient_required
@login_required
def schedule_appointment(request):
    user_profile = request.user.userprofile  # Access the UserProfile
    patient = user_profile.patient  # Access the Patient through UserProfile

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient  # This links the appointment to the specific patient.
            appointment.save()
            return redirect('accounts:patient_dashboard')  # Redirect to view upcoming appointments
    else:
        form = AppointmentForm()

    return render(request, 'appointments/schedule_appointment.html', {'form': form})

@patient_required
@login_required
def patient_dashboard(request):

    user_profile = request.user.userprofile
    patient = user_profile.patient  # Access the Patient through UserProfile
    appointments = patient.appointment_set.all()  # because of foreign key Django provides a way to access all related Appointment objects through the patient instance.
    last_prescription = Prescription.objects.filter(patient=patient).order_by('-date_created').first()  # Get the last prescription

    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments,
        'last_prescription': last_prescription,})

@admin_required
@login_required
def appointments_list_admin(request):

    appointments = Appointment.objects.all()

    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        new_status = request.POST.get('status')
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()
        return redirect('accounts:appointments_list_admin')
    return render(request, 'appointments/appointments_list_admin.html', {'appointments': appointments})

@provider_required
@login_required
def appointments_list_provider(request):
    appointments = Appointment.objects.all()

    return render(request, 'appointments/appointments_list_provider.html', {'appointments': appointments})

@provider_required
@login_required
def prescription_view(request):
    prescriptions = Prescription.objects.all()  # Get all prescriptions

    return render(request, 'prescription/prescription_view.html', {'prescriptions': prescriptions})

@provider_required
@login_required
def add_prescription(request):

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()
            return redirect('accounts:prescription_view')  # Redirect to the same page after saving
    else:
        form = PrescriptionForm()

    return render(request, 'prescription/prescription_form.html', {'form': form})

@provider_required
@login_required
def edit_prescription(request, prescription_id):

    prescription = get_object_or_404(Prescription, id=prescription_id)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            prescription.save()

            return redirect('accounts:prescription_view')  # Redirect to the prescription view after saving
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, 'prescription/prescription_form.html', {'form': form})

@provider_required
@login_required
def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    prescription.delete()
    return redirect('accounts:prescription_view')  # Redirect back to the prescription view

@provider_required
@login_required
def pharmacy(request):
    return render(request,'prescription/pharmacy.html')
