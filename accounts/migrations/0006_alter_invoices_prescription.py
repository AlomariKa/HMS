# Generated by Django 5.1.6 on 2025-03-03 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_invoices_patient_remove_invoices_provider'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoices',
            name='prescription',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.prescription'),
        ),
    ]
