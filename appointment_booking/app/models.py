from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    max_tokens_per_day = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    department = models.ForeignKey(Department, related_name='doctors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    password = models.TextField()
    email = models.EmailField(unique=True,)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    appointment_datetime = models.DateTimeField(default=timezone.now)
    token_number = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        # Generate a token number
        if not self.token_number:
            today = timezone.now().date()
            appointment_count = Appointment.objects.filter(department=self.department, appointment_datetime__date=today).count() + 1
            if appointment_count > self.department.max_tokens_per_day:
                raise ValueError(f"Token limit for today has been reached for the {self.department.name} department.")
            self.token_number = f"{self.department.id}-{today.strftime('%Y%m%d')}-{appointment_count:03d}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_name} - {self.token_number}"

    

class Token(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(default=timezone.now)
    token_number = models.CharField(max_length=255, unique=True)  # Token Number
    patient_name = models.CharField(max_length=255)
    appointment_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Token {self.token_number} for {self.patient_name}"
    


class Patient(models.Model):
    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.TextField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    pincode = models.CharField(max_length=10)

    # Medical Information
    blood_group = models.CharField(max_length=5, blank=True, null=True)  # Optional blood group
    medical_history = models.TextField(blank=True, null=True)  # Brief medical history
    allergies = models.TextField(blank=True, null=True)  # Any known allergies
    current_medication = models.TextField(blank=True, null=True)  # List of medications, if applicable

    # Emergency Information
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)

    # Date and Time Fields
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['last_name', 'first_name']


class Prescription(models.Model):
    # Connect to the Patient model
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')

    # Doctor and Prescription Information
    doctor_name = models.CharField(max_length=255)
    medications = models.TextField(help_text="List the medications prescribed.")
    dosage_instructions = models.TextField(help_text="Instructions for the dosage.")
    
    # Prescription Validity
    date_prescribed = models.DateTimeField(auto_now_add=True)
    validity_date = models.DateField(help_text="Date until the prescription is valid.")

    # Additional notes
    notes = models.TextField(blank=True, null=True, help_text="Any additional notes from the doctor.")

    def __str__(self):
        return f"Prescription for {self.patient.first_name} {self.patient.last_name} by Dr. {self.doctor_name}"

    class Meta:
        ordering = ['date_prescribed']