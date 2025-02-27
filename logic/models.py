# Classes/models.py

from django.db import models
from accounts.models import UserProfile

class Patient(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)  # Allow null
    age = models.IntegerField(blank=True, null=True)  # Allow null
    medical_history = models.TextField(blank=True, null=True)  # Allow null
    allergies = models.TextField(blank=True, null=True)  # Allow null
    insurance_detail = models.TextField(blank=True, null=True)  # Allow null

    def __str__(self):
        return f"Patient: {self.name}"

class AdministrativeStaff(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null=True)
    contact_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"Admin: {self.name}"

class HealthcareProvider(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    specialization = models.CharField(max_length=100, null=True)  # e.g., Doctor, Nurse
    contact_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appointment with {self.provider.name} on {self.date} at {self.time}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.provider.name}"