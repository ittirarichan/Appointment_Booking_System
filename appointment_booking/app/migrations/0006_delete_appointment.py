# Generated by Django 5.1.3 on 2025-01-13 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_appointment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]