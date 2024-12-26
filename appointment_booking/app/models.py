from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    password = models.TextField()


class Doctor(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    password = models.TextField()


class Staff(models.Model):
    email=models.EmailField(unique=True)
    password=models.TextField()
