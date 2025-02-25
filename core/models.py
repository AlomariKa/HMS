from django.db import models
# contains classes for defining your data models from django library
from django.contrib.auth.models import User
# imports the built-in User model provided by Django's authentication system.
# It includes user-related fields like username, password, email, etc.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # creates a one-to-one relationship with the User model. Each profile is linked to one user,
    # and if the user is deleted, the profile will also be deleted
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # create a many-to-one relationship, meaning many Appointment records can be associated with one Patient.
    # Each appointment is associated with one patient
    # if a patient is deleted, all associated appointments are also deleted.
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField
    time = models.TimeField
    status = models.CharField(max_length=20, default="Scheduled")

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.patient.name} - {self.medication}"

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service_description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # max_digits=10: max # digits store. both digits to the left and right of the decimal point.
    # decinmal_places:  # decimal places to store. (12345678.99)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.patient.name} - {self.service_description}"