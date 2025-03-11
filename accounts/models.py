from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('admin', 'Administrative Staff'),
        ('provider', 'Healthcare Provider'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    @property
    def is_patient(self):
        return self.user_type == 'patient'

    @property
    def is_admin(self):
        return self.user_type == 'admin'

    @property
    def is_provider(self):
        return self.user_type == 'provider'




# Create a signal to create/update the user profile
# Django signals to automatically create or update a UserProfile whenever a User instance is created or saved.

# This signal creates a UserProfile when a new User instance is created:

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Patient(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    allergies =  models.TextField(blank=True, null=True)
    insurance_detail =  models.TextField(blank=True, null=True)

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
    specialization = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # On patient have multiple appointments
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('provider', 'date', 'time')
        # Meta is an inner class you can define inside a model to configure the behavior of the model.
        # It provides options (called "metadata") that control various aspects of how the model interacts with
        # the database, admin interface, and Django framework.

    def __str__(self):
        return f"Appointment with {self.provider.name} on {self.date} at {self.time}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    provider = models.ForeignKey(HealthcareProvider, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    medication = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()
    service_description = models.TextField(max_length=255 , null=True)
    send = models.BooleanField(default=False)

    def __str__(self):
        return f"prescription for {self.patient.name} by {self.provider.name}"

class Invoices(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )
    prescription = models.OneToOneField(Prescription, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    Insurance_percent_cover = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.patient_name}"

class DeviceData(models.Model):
    patient_id = models.CharField(max_length=10, null=True)
    heart_rate = models.IntegerField()
    blood_pressure = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.timestamp}"