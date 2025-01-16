from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import *

from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings

import hashlib  #for password hashing
from .models import Department,Appointment, Doctor,Patient # Import models explicitly
import random
import string

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.core.exceptions import PermissionDenied








def appointment_login(req):
    # Initialize email and password to None
    email = None
    password = None

    # Check if the user is already logged in
    if 'doctor' in req.session:
        return redirect(doc_home)  
    
    # if 'staff' in req.session:
    #     return redirect(staff_home)  
    
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

        # try:
        #     staff = Staff.objects.get(email=email, password=password)
        #     req.session['staff'] = staff.email  # Store staff session
        #     return redirect(staff_home)  # Redirect to staff home page
        # except Staff.DoesNotExist:
        #     pass  # Continue if staff is not found


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
    # if 'staff' in req.session:
    #     del req.session['staff']
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


        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
        data = Patient.objects.create(name=name, email=email, password=password)
  #(model=variable)
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



def add_Specialization(request):
    if request.method == 'POST':
        dep_name = request.POST['dep_name']
        Department.objects.create(name=dep_name.upper())
        dep = Department.objects.all()  # Use 'departments' instead of 'Department'
    # Your other logic goes here
        return redirect(add_Specialization)
    else:
        dep = Department.objects.all()
        return render(request, 'admin/add_department.html', {'Departments': dep})
    

def delete_Specialization(req, id):
    if 'admin' in req.session:
        try:
            department = Department.objects.get(id=id)
            department.delete()
            messages.success(req, "Department successfully deleted.")
        except Department.DoesNotExist:
            messages.error(req, "Department not found.")
        return redirect(add_Specialization)  # Make sure `add_Specialization` is defined elsewhere
    else:
        return redirect(appointment_login)  # Make sure `appointment_login` is defined elsewhere







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



# def register_staff(request):
#     if request.method == 'POST':
#         # Get the data from the form
#         # username = request.POST.get('username')
#         email = request.POST.get('email')
        
#         if email:
#             # Generate a random password
#             password = generate_random_password()

#             # data = Staff.objects.create(email=email, password=password)
            
#             try:
#                 send_mail(
#                     'Your Account Details',
#                     f"Your account has been created. Your password is: {password}",
#                     settings.EMAIL_HOST_USER,
#                     [email],
#                     fail_silently=False
#                 )
#             except Exception as e:
#                 messages.error(request, f"Error sending email: {e}")


#             messages.success(request, "Staff member created successfully! The password has been sent to their email." )
#             return redirect(admin_home)  # Redirect to admin dashboard or another page
#         else:
#             messages.error(request, "Please provide email.")
    
#     return render(request, 'admin/register_staff.html')







def register_doctor(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        department_id = request.POST.get('spec_name')  # Renamed to department_id for clarity

        try:
            # Get the department object (used as specialization in the Doctor model)
            department = Department.objects.get(id=department_id)

            # Check if email is provided
            if email:
                # Generate a random password
                password = generate_random_password()

                # Create a new doctor record in the database
                doctor = Doctor.objects.create(
                    name=name,
                    email=email,
                    department=department,  # Store the department as specialization
                    password=password
                )

                # Send the password to the doctor via email
                send_mail(
                    'Your Doctor Account Details',
                    f'Hello {name},\n\nYour Doctor account has been created. Your password is: {password}\nPlease change it after logging in.',
                    'abhishekbinish86@gmail.com',  # Replace with your email
                    [email],
                    fail_silently=False,
                )

                # Success message and redirect to admin dashboard
                messages.success(request, "Doctor member created successfully! The password has been sent to their email.")
                return redirect(admin_home)  # Make sure 'admin_home' URL is defined correctly

            else:
                # Error if email is missing
                messages.error(request, "Please provide an email.")
        except Department.DoesNotExist:
            # Handle the case when the department is not found
            messages.error(request, "Invalid department selected. Please try again.")

    # Fetch departments to display in the form
    departments = Department.objects.all()

    return render(request, 'admin/register_doc.html', {'departments': departments})





# ----------------------------------------------------token--------------------------------------------------------------------------
# def book_appointment(request):
#     if request.method == 'POST':
#         name=request.POST['name']
#         email=request.POST['email']
#         age=request.POST['age']
#         gender=request.POST['gender']
#         phone=request.POST['phone']
#         address=request.POST['address']
#         appointment_date=request.POST['appointment_date']
#         department_id=request.POST['department']
#         doctor_id=request.POST['doctor']

#         department = Department.objects.get(id=department_id)
#         doctor = Doctor.objects.get(id=doctor_id)
        
  
#         appointment = Appointment.objects.create(name=name,email=email,age=age,gender=gender,phone=phone,address=address,department=department,
#                                                  doctor=doctor,appointment_date=appointment_date)
#         appointment.save()
#     else:
#         # Fetch categories and brands to populate dropdowns
#         doctor = Doctor.objects.all()
#         department = Department.objects.all()
#         return render(request, 'user/quick_appointmnet.html', {'doctor': doctor, 'department': department})
        

def book_appointment(request):
    patient_email = request.session.get('patient')
    if not patient_email:
        return redirect('login')  # Redirect to login if no session data for patient

    try:
        # Retrieve the patient instance based on the session email
        patient = Patient.objects.get(email=patient_email)
    except Patient.DoesNotExist:
        return redirect('login')  # If the patient does not exist, redirect to login

    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST['age']
        gender = request.POST['gender']
        blood_group = request.POST['bgroup']
        phone = request.POST['phone']
        address = request.POST['address']
        pincode = request.POST['pin']
        appointment_date = request.POST['appointment_date']
        department_id = request.POST['department']
        doctor_id = request.POST['doctor']

        # Get the department and doctor objects
        department = Department.objects.get(id=department_id)
        doctor = Doctor.objects.get(id=doctor_id)

        # Check how many appointments have already been booked for this doctor on the given appointment date
        appointment_count = Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date).count()

        # If the appointment count exceeds the max token limit for the department, raise an error
        if appointment_count >= doctor.department.max_tokens_per_day:
            return render(request, 'user/quick_appointment_error.html', {
                'error': f"Cannot book more than {doctor.department.max_tokens_per_day} appointments for this department on this day."
            })

        # Generate the token number for this appointment
        token_number = appointment_count + 1  # Token numbers start from 1, incrementing with each appointment

        # Update the patient details (only if the patient exists)
        patient.name = name
        patient.age = age
        patient.gender = gender
        patient.blood_group = blood_group
        patient.phone = phone
        patient.address = address
        patient.pincode = pincode
        patient.save()  # Save the updated patient details

        # Create the appointment with the generated token number and the patient instance
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,  # Ensure patient is linked to the appointment
            appointment_date=appointment_date,
            department=department.name,  # Store the department name
            token_number=token_number
        )

        # Return the success page with the generated appointment details
        # return render(request, 'user/appointment_success.html', {'appointment': appointment.token_number})
        return redirect(appointment_success)  # Redirect to the success page

    else:
        # Fetch doctors and departments to populate dropdowns
        doctors = Doctor.objects.all()
        departments = Department.objects.all()
        return render(request, 'user/quick_appointment.html', {'doctors': doctors, 'departments': departments, 'patient': patient})






def get_doctors(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id)
    doctor_list = [{'id': doctor.id, 'name': doctor.name} for doctor in doctors]
    return JsonResponse({'doctors': doctor_list})


def appointment_success(request):
    email = request.session.get('patient')
    
    if not email:
        # Redirect if no session exists for 'patient'
        return redirect('login')  # Assuming you have a login view
    
    # Fetch the patient from the email
    try:
        patient = Patient.objects.get(email=email)
    except Patient.DoesNotExist:
        # Handle case where the patient doesn't exist
        return redirect('login')
    
    # Fetch all appointments for the patient, ordered by appointment date
    appointments = Appointment.objects.filter(patient=patient).order_by('appointment_date')[::-1]
    # prescription = Prescription.objects.filter(patient=patient)
    
    if not appointments:
        # Handle case where no appointments exist for the patient
        return render(request, 'user/appointment_success.html', {'message': 'No appointments found.'})
    
    # Render the appointment success page with the list of appointments
    return render(request, 'user/appointment_success.html', {'appointments': appointments})









def view_prescription(request):
    email = request.session.get('patient')
    
    if not email:
        # Redirect if no session exists for 'patient'
        return redirect('login')  # Assuming you have a login view
    
    try:
        # Fetch the patient from the email
        patient = Patient.objects.get(email=email)
    except Patient.DoesNotExist:
        # Handle case where the patient doesn't exist
        return redirect('login')
    
    # Fetch all prescriptions for the patient
    prescriptions = Prescription.objects.filter(patient=patient)[::-1]
    
    if not prescriptions:
        # Handle case where no prescriptions exist for the patient
        return render(request, 'user/view_prescription.html', {'message': 'No prescriptions found.'})
    
    # Render the view prescription page with the list of prescriptions
    return render(request, 'user/view_prescription.html', {'prescriptions': prescriptions})









def user_services(req):
    if 'patient' in req.session:
        return render(req,'user/services.html')
    else:
        return redirect(appointment_login)






def user_home(request):
    """Show user home page with their latest appointment."""
    if 'patient' not in request.session:
        return redirect(appointment_login)
        
    try:
        appointment = Appointment.objects.filter(
            email=request.session['patient']
        ).order_by('-created_at').first()
    except Exception as e:
        print(f"Error fetching appointment: {e}")
        appointment = None
        
    return render(request, 'user/index.html', {'appointment': appointment})



def doc_home(req):
    if 'doctor' in req.session:
        doctor=Doctor.objects.get(email=req.session['doctor'])  # Assuming you store the doctor's email in the session
        return render(req, 'doctor/doc_home.html',{'doctor':doctor})
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











def doctor_appointments_view(req):
    if 'doctor' in req.session:
        try:
            doctor = Doctor.objects.get(email=req.session['doctor'])  # Assuming you store the doctor's email in the session
        except Doctor.DoesNotExist:
            return redirect(appointment_login)  # Redirect to the login page if the doctor is not found
        
        # Get today's date in the local timezone
        today = timezone.localdate()
        
        # Fetch today's appointments for the logged-in doctor
        appointments = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today  # Filter by today's date
        ).order_by('-appointment_date')
        
        # Render the appointments page with the doctor's appointments
        return render(req, 'doctor/appointments.html', {'appointments': appointments})
    
    else:
        return redirect(appointment_login)  # Redirect if 'doctor' session does not exist





def view_patient_details(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    # Check if the session contains a 'doctor' key
    if 'doctor' not in request.session:
        # If no 'doctor' key is found in the session, raise a PermissionDenied error or handle as needed
        raise PermissionDenied("You do not have the necessary permissions to view this page.")

    # Get the doctor from the session
    doctor = Doctor.objects.get(email=request.session['doctor'])   # This assumes 'doctor' in session is an ID or a doctor object

    # Fetch or create the prescription, ensuring the doctor is provided
    prescription, created = Prescription.objects.get_or_create(patient=patient, doctor=doctor)

    if request.method == 'POST':
        # Update prescription data from POST request
        medications = request.POST.get('medications', '')
        notes = request.POST.get('notes', '')
        prescription.medications = medications
        prescription.notes = notes
        prescription.date_prescribed = timezone.now()
        prescription.save()

        # Redirect back to the patient's details page
        return redirect(doctor_appointments_view)

    # Render the patient's details along with the prescription
    return render(request, 'doctor/patient_details.html', {'patient': patient, 'prescription': prescription}) 






def admin_view_appointments(req):
    appointments=Appointment.objects.all()[::-1]
    return render( req,'admin/appointments.html',{'appointments':appointments})



def view_all_patient(req):
    patient=Patient.objects.all()[::-1]
    return render( req,'admin/all_patients.html',{'patient':patient})

def view_all_doctors(req):
    doc=Doctor.objects.all()[::-1]
    return render( req,'admin/all_doctors.html',{'doc':doc})


def view_all_prescription(req):
    pre=Prescription.objects.all()[::-1]
    return render( req,'admin/all_prescriptions.html',{'pre':pre})