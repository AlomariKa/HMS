# Generated by Django 5.2b1 on 2025-03-10 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_remove_devicedata_patient_id_devicedata_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicedata',
            name='patient',
        ),
        migrations.AddField(
            model_name='devicedata',
            name='patient_id',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
