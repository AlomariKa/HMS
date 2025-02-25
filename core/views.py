from django.shortcuts import render,get_object_or_404
# render: A shortcut function to render an HTML template with a context.
# get_object_or_404: A function that retrieves an object from the database if it exists or returns a 404 error if it doesn't.
from .models import Patient, Doctor, Appointment, Prescription, Billing

def patient_dashboard(request):
    # takes an HTTP request as a parameter.
    patient = get_object_or_404(Patient, user=request.user)
    # Fetch a Patient object that matches the currently logged-in user (request.user)
    appointments = Appointment.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)
    # Show me all the appointments that belong to this particular patient.
    return render(request,'patient_dashboard.html', {'patient': patient, 'appointments': appointments, 'prescriptions': prescriptions})
# dictionary containing the context data you want to pass to the template. Each key-value pair in the dictionary becomes a variable in the template.
# 'patient': This key is paired with the patient object. The template can access the patient's details using this variable

def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)

    return render(request,'doctor_dashboard.html',{'doctor':doctor,'appointments':appointments})

def schedule_appointment(request):
    if request.method == 'POST':
        # Handle appointment scheduling logic
        pass
    return render(request, 'schedule_appointment.html')