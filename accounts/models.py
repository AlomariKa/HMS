from django.contrib.auth.models import User
# Django’s built-in user model
from django.db import models
# create and manage database models.

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        # first value is stored in the database,
        # and the second value is the human-readable name.
        ('patient', 'Patient'),
        ('admin', 'Administrative Staff'),
        ('provider', 'Healthcare Provider'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Each user has exactly one UserProfile, and the profile has exactly one user.
    # If a user is deleted, their profile will also be deleted
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)



# Create a signal to create/update the user profile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User) # connects post_save signal to the create_user_profile function for User model.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


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
        return f"Prescription for {self.patient.name} by {self.provider.name}"

class Invoices(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )
    prescription = models.OneToOneField(Prescription, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    total_amount = models.FloatField()
    Insurance_percent_cover = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')