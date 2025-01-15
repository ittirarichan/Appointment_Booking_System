from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    max_tokens_per_day = models.IntegerField(default=100)


class Doctor(models.Model):
    department = models.ForeignKey(Department, related_name='doctors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    password = models.TextField()
    email = models.EmailField(unique=True,)

 

    


class Patient(models.Model):
    name = models.CharField(max_length=50)
    password = models.TextField()
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5, blank=True, null=True)  # Optional blood group
    date_created = models.DateTimeField(auto_now_add=True, null= True)
    last_updated = models.DateTimeField(auto_now=True, null= True)

 

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medications = models.TextField(help_text="List the medications prescribed.")
    # qty = models.CharField(max_length=100, help_text="Quantity of the medication prescribed.")
    date_prescribed = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="Any additional notes from the doctor.")

  
    

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    token_number = models.IntegerField()
    department = models.CharField(max_length=50)
