# Generated by Django 5.2b1 on 2025-03-10 18:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_devicedata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicedata',
            name='patient_id',
        ),
        migrations.AddField(
            model_name='devicedata',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.patient'),
        ),
    ]
