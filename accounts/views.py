# accounts/views.py
import csv

from django.contrib.auth import login, authenticate, logout # These functions are used for handling user authentication, logging users in and out.
from django.contrib import messages # This module is used to display messages to users.
from django.db.models import Sum,F
from django.http import HttpResponse
from django.shortcuts import render, redirect , get_object_or_404
from .forms import PatientForm, AdministrativeStaffForm, HealthcareProviderForm,AppointmentForm,PrescriptionForm,UserRegisterForm, InvoicesForm
from .models import UserProfile,Appointment,Patient, AdministrativeStaff,HealthcareProvider,Prescription,Invoices,DeviceData
from django.contrib.auth.decorators import login_required
from .decorators import provider_required,admin_required,patient_required, new_provider_required,new_admin_required,new_patient_required
from .serializers import DeviceDataSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response





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

@patient_required
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


@patient_required
@login_required # ensures that only authenticated users can acces
def patient_profile(request):
    try:
        user_profile = request.user.userprofile  # Access the UserProfile
        patient = user_profile.patient

    except Patient.DoesNotExist:
        # Redirect to profile creation page if the user does not have a Patient profile
        return redirect('accounts:create_patient_profile')  # You need to create this view

    if not hasattr(request.user, 'userprofile') or not hasattr(request.user.userprofile, 'patient'):
        #hasattr check if an object has a specific attribute
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


@admin_required
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

@provider_required
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
    appointments = patient.appointment_set.select_related('patient').all()  # because of foreign key Django provides a way to access all related Appointment objects through the patient instance.
    last_prescription = Prescription.objects.select_related('patient').filter(patient=patient).order_by('-date_created').first()  # Get the last prescription
    prescriptions = patient.prescription_set.select_related('patient').all()

    # prescription_send_values = [prescription.send for prescription in prescriptions]
    # print(prescription_send_values)
    # for send_value in prescription_send_values:
    #     print("----")
    #     print(send_value)
    #     print("----")

    return render(request, 'appointments/patient_dashboard.html', {'appointments': appointments,
        'last_prescription': last_prescription, "prescriptions":prescriptions})

@admin_required
@login_required
def appointments_list_admin(request):

    appointments = Appointment.objects.select_related('patient','provider').all()

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
    appointments = Appointment.objects.select_related('patient','provider').all()

    return render(request, 'appointments/appointments_list_provider.html', {'appointments': appointments})

@provider_required
@login_required
def prescription_view(request):
    prescriptions = Prescription.objects.select_related('patient','provider').all()  # Get all prescriptions

    return render(request, 'prescription/prescription_view.html', {'prescriptions': prescriptions})

@provider_required
@login_required
def add_prescription(request):

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            # created but not saved immediately (commit=False). This allows additional changes if needed.
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

    if request.method == 'POST':
        prescription = get_object_or_404(Prescription, id=prescription_id)
        prescription.delete()

        return redirect('accounts:prescription_view')  # Redirect to the prescription view after saving
    # prescription = get_object_or_404(Prescription, id=prescription_id)
    # prescription.delete()
    # return redirect('prescription_view')

    return render(request, 'prescription/prescription_confirm_delete.html', {'prescription': prescription})

@provider_required
@login_required
def pharmacy(request,prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    prescription.send = True
    prescription.save()
    return render(request,'prescription/pharmacy.html')

@admin_required
@login_required
def invoice_view(request):
    invoices = Invoices.objects.select_related('prescription').all()
    for invoice in invoices:
        invoice.payable_amount = invoice.total_amount * (1 - (invoice.Insurance_percent_cover / 100))
    return render(request,'invoices/invoice_view.html', {'invoices': invoices})

@admin_required
@login_required
def add_invoice(request):

    if request.method == 'POST':
        form = InvoicesForm(request.POST)
        if form.is_valid():

            invoice = form.save(commit=False)
            invoice.save()

            return redirect('accounts:invoice_view')  # Redirect to the same page after saving
    else:
        form = InvoicesForm()


    return render(request,'invoices/invoice_form.html', {'form': form})

@admin_required
@login_required
def edit_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoices, id=invoice_id)

    if request.method == 'POST':
        form = InvoicesForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            invoice.save()

            return redirect('accounts:invoice_view')
    else:
        form = InvoicesForm(instance=invoice)

    return render(request, 'invoices/invoice_form.html', {'form': form})

@admin_required
@login_required
def invoice_detail(request,invoice_id):
    invoice = get_object_or_404(Invoices, id=invoice_id)
    invoice.insurance_cover = (invoice.total_amount) * (invoice.Insurance_percent_cover / 100)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})

@admin_required
@login_required
def invoice_pay(request,invoice_id):
    invoice = get_object_or_404(Invoices, id=invoice_id)
    invoice.status = 'paid'
    invoice.save()
    return redirect('accounts:invoice_view')

@admin_required
@login_required
def delete_invoice(request,invoice_id):

    invoice = get_object_or_404(Invoices, id=invoice_id)

    if request.method == 'POST':
        invoice = get_object_or_404(Invoices, id=invoice_id)
        invoice.delete()

        return redirect('accounts:invoice_view')  # Redirect to the prescription view after saving

    return render(request, 'invoices/invoice_confirm_delete.html', {'invoice': invoice})

@admin_required
@login_required
def patients_insurance(request):
    patients = Patient.objects.all()

    return render(request,'invoices/patients_insurance.html', {'patients':patients})

@admin_required
@login_required
def service_description(request):
    services = Prescription.objects.all()
    return render(request,'invoices/service_description.html', {'services':services})


@login_required
@admin_required  # Ensure only admins can access this view
def reporting_dashboard(request):

    # Initialize variables for the report

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_type = request.GET.get('report_type')


    # Filter data based on the date range
    appointments = Appointment.objects.select_related('patient','provider').all()
    if start_date and end_date:
        appointments = appointments.filter(date__range=[start_date, end_date])

    total_visits = appointments.count()

    invoices = Invoices.objects.select_related('prescription').all()
    total_revenue = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0 # common way to calculate the total sum of a field in a Django QuerySet using the Django ORM
    insurance_revenue = invoices.annotate(weighted_value=F('total_amount') * F('Insurance_percent_cover')/100).aggregate(Sum('weighted_value'))['weighted_value__sum'] or 0
    insurance_revenue = round(insurance_revenue, 2)

    patient_revenue = total_revenue - insurance_revenue


    # Prepare data for charts (you can customize this as needed)
    chart_data = {
        'total_visits': total_visits,
        'total_revenue': total_revenue,
        'insurance_revenue':insurance_revenue,
        'patient_revenue':patient_revenue
    }

    return render(request, 'reports/reporting_dashboard.html', {
        'chart_data': chart_data,
        'start_date': start_date,
        'end_date': end_date,
        'report_type': report_type,
        'appointments':appointments
    })

@login_required
@admin_required
def download_report_summary(request):
    response = HttpResponse(content_type='text/csv') # send HTTP responses back to the client // response is a CSV file.
    response['Content-Disposition'] = 'attachment; filename="report.csv"' # treat the response as a file attachment and prompts the user to download it with the filename report.csv.

    writer = csv.writer(response) # interface for writing CSV data into a file-like object
    writer.writerow(['Patient', 'Provider'])  # Header row

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    appointments = Appointment.objects.all()
    if start_date and end_date:
        appointments = appointments.filter(date__range=[start_date, end_date])

    for appointment in appointments:
        writer.writerow([appointment.patient.name, appointment.provider])

    return response

@login_required
@admin_required
def download_report_detail(request):
    response = HttpResponse(content_type='text/csv') # send HTTP responses back to the client // response is a CSV file.
    response['Content-Disposition'] = 'attachment; filename="report.csv"' # treat the response as a file attachment and prompts the user to download it with the filename report.csv.

    writer = csv.writer(response) # interface for writing CSV data into a file-like object
    writer.writerow(['Patient', 'Provider','Date', 'Time','Status' ])  # Header row

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    appointments = Appointment.objects.all()
    if start_date and end_date:
        appointments = appointments.filter(date__range=[start_date, end_date])

    for appointment in appointments:
        writer.writerow([appointment.patient.name, appointment.provider, appointment.date, appointment.time,appointment.status])

    return response


@admin_required
@login_required
def download_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoices, id=invoice_id)

    # Set the response type to CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{invoice.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['Invoice ID', 'Patient Name', 'Total Amount', 'Insurance Cover', 'Payable Amount', 'Status', 'Date Created'])

    # Calculate Payable Amount
    insurance_cover = invoice.total_amount * (invoice.Insurance_percent_cover / 100)
    payable_amount = invoice.total_amount - insurance_cover

    # Write Invoice Data
    writer.writerow([
        invoice.id,
        invoice.prescription.patient.name,
        invoice.total_amount,
        insurance_cover,
        payable_amount,
        invoice.status,
        invoice.date_created
    ])

    return response

@login_required
@admin_required
def download_revenue(request):
    response = HttpResponse(content_type='text/csv') # send HTTP responses back to the client // response is a CSV file.
    response['Content-Disposition'] = 'attachment; filename="revenue.csv"' # treat the response as a file attachment and prompts the user to download it with the filename report.csv.

    writer = csv.writer(response) # interface for writing CSV data into a file-like object
    writer.writerow(['Total Revenue', 'Insurance Revenue','Patient Revenue'])  # Header row

    invoices = Invoices.objects.all()
    total_revenue = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0  # common way to calculate the total sum of a field in a Django QuerySet using the Django ORM
    insurance_revenue = invoices.annotate(weighted_value=F('total_amount') * F('Insurance_percent_cover') / 100).aggregate(Sum('weighted_value'))['weighted_value__sum'] or 0
    insurance_revenue = round(insurance_revenue, 2)

    patient_revenue = total_revenue - insurance_revenue

    writer.writerow([total_revenue, insurance_revenue,patient_revenue])

    return response


@api_view(['POST'])
def receive_device_data(request):
    # Create a serializer instance with the incoming data
    serializer = DeviceDataSerializer(data=request.data)

    # Check if the data is valid
    if serializer.is_valid():
        # Save the valid data to the database
        serializer.save()

        # Return a 201 Created response with the serialized data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # If the data is invalid, return a 400 Bad Request response with error details
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def device_data_view(request):
    # Retrieve all device data along with the related patient names
    device_data = DeviceData.objects.all()
    # Check if there is any device data
    if not device_data:
        message = "No device data available."
    else:
        message = None  # No message if data is available

    # Render the HTML template with the device data and message
    return render(request, 'device_data.html', {'device_data': device_data, 'message': message})