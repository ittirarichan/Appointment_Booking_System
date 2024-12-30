from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *
import os
import re
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings

import hashlib  #for password hashing
from .models import Patient, Doctor, Staff
import random
import string



def appointment_login(req):
    # Initialize email and password to None
    email = None
    password = None

    # Check if the user is already logged in
    if 'doctor' in req.session:
        return redirect(doc_home)  
    
    if 'staff' in req.session:
        return redirect(staff_home)  
    
    if 'patient' in req.session:
        return redirect(user_home) 
     
    if 'admin' in req.session:
        return redirect(user_home)  




    if req.method == 'POST':
        email = req.POST.get('email')  # Get email from POST request
        password = req.POST.get('password')  # Get password from POST request

        # ---------Patientlog-----------        
        try:
            # Check for user in User_Register model (custom user model)
            user = Patient.objects.get(email=email, password=password)
            req.session['patient'] = user.email  # Store user session
            return redirect(user_home)  # Redirect to user home page
        except Patient.DoesNotExist:
            pass


        # ---------doctorlog-----------        

        try:
            doctor = Doctor.objects.get(email=email, password=password)
            req.session['doctor'] = doctor.email  # Store doctor session
            return redirect(doc_home)  # Redirect to doctor home page
        except Doctor.DoesNotExist:
            pass  # Continue to the next check if doctor is not found


        # ---------stafflog-----------        

        try:
            staff = Staff.objects.get(email=email, password=password)
            req.session['staff'] = staff.email  # Store staff session
            return redirect(staff_home)  # Redirect to staff home page
        except Staff.DoesNotExist:
            pass  # Continue if staff is not found


        # ---------adminlog-----------        
        admin = authenticate(username=email, password=password)  # Use Django's built-in authentication for admin
        if admin is not None:
            login(req, admin)  # Django login
            req.session['admin'] = email  # Store admin session
            return redirect(admin_home)  # Redirect to admin home page
        else:
            messages.warning(req, "Invalid username or password.")
            return redirect(appointment_login)  # Reload login page if invalid credentials
    return render(req, 'sign_in_&_up.html')



# ------------------------------logout------------------------------


def logout(req):
    if 'patient' in req.session:
        # req.session.flush()
        del req.session['patient']
    if 'staff' in req.session:
        del req.session['staff']
    if 'doctor' in req.session:
        del req.session['doctor']
    if 'admin' in req.session:
        del req.session['admin']
    return redirect(appointment_login)



# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------



# ------------------------------Registrations------------------------------


def user_register(req):
    if req.method=='POST':
        name=req.POST['name_reg']
        email=req.POST['email_reg']
        password=req.POST['password_reg']

        
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            messages.warning(req, "Invalid email format, please enter a valid email.")
            return render(req,'sign_in_&_up.html')

        # Validate phone number (assuming 10-digit numeric format)
        # if not re.match(r'^\d{10}$', ):
        #     messages.warning(req, "Invalid phone number. Please enter a valid 10-digit phone number.")
        #     return render(req, 'sign_in_&_up.html')
        # try:
        data=Patient.objects.create(name=name,email=email,password=password)  #(model=variable)
        data.save()
        subject = 'Registration details '
        message = 'Your account username: {}  and password: {}'.format(name,password)
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list,fail_silently=False)  
        return redirect(appointment_login)
        # except:
        # messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'sign_in_&_up.html')



def add_Specialization(req):
    if 'admin' in req.session:
        if req.method == 'POST':
            dep_name = req.POST['dep_name']
            Specialization.objects.create(spec_name=dep_name.upper())
            specialization = Specialization.objects.all()
            return render(req, 'admin/add_department.html', {'Department': specialization})
        else:
            specialization = Specialization.objects.all()
            return render(req, 'admin/add_department.html', {'Department': specialization})
    else:
        return redirect(appointment_login)
    

def delete_Specialization(req, id):
    if 'admin' in req.session:
        try:
            Department = Specialization.objects.get(id=id)
            Department.delete()
        except Specialization.DoesNotExist:
            pass  # You can add an error message here if needed
        return redirect(add_Specialization)
    else:
        return redirect(appointment_login)
    








# def generate_password(length=8):
#     # Define characters to use
#     characters = string.ascii_letters + string.digits + "!@#$%^&*"
    
#     # Generate password
#     password = ''.join(random.choice(characters) for _ in range(length))
#     return password





def generate_random_password(length=8):
    """Generate a random password with letters and digits."""
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password



def register_staff(request):
    if request.method == 'POST':
        # Get the data from the form
        # username = request.POST.get('username')
        email = request.POST.get('email')
        
        if email:
            # Generate a random password
            password = generate_random_password()

            # Create a new user (staff member)
            data = Staff.objects.create(email=email, password=password)
            
            # Send the password to the staff via email
            send_mail(
                'Your Staff Account Details',
                f'Hello {email},\n\nYour staff account has been created. Your password is: {password}\nPlease change it after logging in.',
                'abhishekbinish86@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            messages.success(request, "Staff member created successfully! The password has been sent to their email.")
            return redirect(admin_home)  # Redirect to admin dashboard or another page
        else:
            messages.error(request, "Please provide email.")
    
    return render(request, 'admin/register_staff.html')







def register_doctor(request):
    if request.method == 'POST':
        # Get the data from the form
        # username = request.POST.get('username')
        email = request.POST.get('email')
        spec_name_id =request.POST.get('spec_name')

        spec=Specialization.objects.get(id=spec_name_id)
        
        if email:
            # Generate a random password
            password = generate_random_password()

            # Create a new user (staff member)
            data = Doctor.objects.create(email=email,specialization=spec, password=password)
            data.save()
            
            # Send the password to the staff via email
            send_mail(
                'Your Doctor Account Details',
                f'Hello {email},\n\nYour Doctor account has been created. Your password is: {password}\nPlease change it after logging in.',
                'abhishekbinish86@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            messages.success(request, "Doctor member created successfully! The password has been sent to their email.")
            return redirect(admin_home)  # Redirect to admin dashboard or another page
        else:
            messages.error(request, "Please provide email.")
    
    departments=Specialization.objects.all()
    return render(request, 'admin/register_doc.html',{'departments':departments})







def user_services(req):
    if 'patient' in req.session:
        return render(req,'user/services.html')
    else:
        return redirect(appointment_login)






def user_home(req):
    if 'patient' in req.session:              #checking section status
        return render(req, 'user/index.html')
    else:
        return redirect(appointment_login)


def doc_home(req):
    if 'doctor' in req.session:              #checking section status
        return render(req, 'doctor/doc_home.html')
    else:
        return redirect(appointment_login)

def staff_home(req):
    if 'staff' in req.session:              #checking section status
        return render(req, 'staff/staff_home.html')
    else:
        return redirect(appointment_login)

def admin_home(req):
    if 'admin' in req.session:              #checking section status
        return render(req, 'admin/admin_home.html')
    else:
        return redirect(appointment_login)
