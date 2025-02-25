from django.contrib import admin
from .models import Patient, Doctor, Appointment, Prescription, Billing

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Billing)