from django.db import models

# Create your models here.
class Patient(models.Model):
    name = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    password = models.TextField()

class Specialization(models.Model):
    spec_name = models.TextField()

class Doctor(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    password = models.TextField()
    phone = models.CharField(max_length=15,null=True)
    specialization=models.ForeignKey(Specialization,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True,null=True)



class Staff(models.Model):
    email=models.EmailField(unique=True)
    password=models.TextField()

