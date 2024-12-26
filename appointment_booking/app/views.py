from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *
import os
import re
from django.contrib.auth.models import User,auth

from django.core.mail import send_mail
from django.conf import settings



# ------------------------------appointment_login------------------------------

def appointment_login(req):
    # Check if the user is already logged in
    if 'doctor' in req.session:
        return redirect(doc_home)
    
    if 'staff' in req.session:
        return redirect(staff_home)
    
    if 'user' in req.session:
        return redirect(user_home)

    if req.method == 'POST':
        email = req.POST['email']
        password = req.POST['password']

        # ---------userlog-----------        
        try:
            # Check for user in User_Register model (custom user model)
            user = User.objects.get(email=email, password=password)
            req.session['user'] = user.Email  # Store user session
            return redirect(user_home)
        except User.DoesNotExist:
            pass  # Continue to the next check if user is not found

        # ---------adminlog-----------        
        admin = authenticate(username=email, password=password)  # Use Django's built-in authentication for admin
        if admin is not None:
            auth(req, admin)  # Django login
            req.session['admin'] = email  # Store admin session
            return redirect(admin_home)

        # ---------doctorlog-----------        
        try:
            doctor = Doctor.objects.get(email=email, password=password)
            req.session['doctor'] = doctor.Email  # Store doctor session
            return redirect(doc_home)
        except Doctor.DoesNotExist:
            pass  # Continue to the next check if doctor is not found

        # ---------stafflog-----------        
        try:
            staff = Staff.objects.get(email=email, password=password)
            req.session['staff'] = staff.Email  # Store staff session
            return redirect(staff_home)
        except Staff.DoesNotExist:
            pass  # Continue if staff is not found

        # If no matching login found, show an error message
        messages.warning(req, "Invalid credentials! Please check your email and password.")
    
    return render(req, 'sign_in_&_up.html')


# ------------------------------logout------------------------------


def logout(req):
    if 'user' in req.session:
        # req.session.flush()
        del req.session['user']
    if 'staff' in req.session:
        del req.session['staff']
    if 'doctor' in req.session:
        del req.session['doctor']
    return redirect(appointment_login)



# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------



# ------------------------------Registrations------------------------------


def user_register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        #  Validate email
        # try:
        #     validate_email(email)
        # except ValidationError:
        #     messages.warning(req, "Invalid email format, please enter a valid email.")
        #     return render(req, 'sign_in_&_up.html')

        # # Validate phone number (assuming 10-digit numeric format)
        # if not re.match(r'^\d{10}$', ):
        #     messages.warning(req, "Invalid phone number. Please enter a valid 10-digit phone number.")
        #     return render(req, 'sign_in_&_up.html')
        # # try:
        data=Patient.objects.create(name=name,email=email,password=password)
        data.save()
        # subject = 'Registration details '
        # message = 'ur account uname {}  and password {}'.format(name,password)
        # from_email = settings.EMAIL_HOST_USER
        # recipient_list = [email]
        # send_mail(subject, message, from_email, recipient_list,fail_silently=False)  
        return redirect(appointment_login)
        # except:
        # messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'sign_in_&_up.html')






def user_home(req):
    return render(req,'user/index.html')


def doc_home(req):
    return render(req,'doctor/doc_home.html')


def staff_home(req):
    return render(req,'staff/staff_home.html')

def admin_home(req):
    return render(req,'user/index.html')
