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
from .models import Department, Doctor, Appointment,Patient # Import models explicitly
import random
import string

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect






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



def register_staff(request):
    if request.method == 'POST':
        # Get the data from the form
        # username = request.POST.get('username')
        email = request.POST.get('email')
        
        if email:
            # Generate a random password
            password = generate_random_password()

            # data = Staff.objects.create(email=email, password=password)
            
            try:
                send_mail(
                    'Your Account Details',
                    f"Your account has been created. Your password is: {password}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")


            messages.success(request, "Staff member created successfully! The password has been sent to their email." )
            return redirect(admin_home)  # Redirect to admin dashboard or another page
        else:
            messages.error(request, "Please provide email.")
    
    return render(request, 'admin/register_staff.html')







def register_doctor(request):
    if request.method == 'POST':
        # Get the data from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        spec_name_id =request.POST.get('spec_name')

        spec=Department.objects.get(id=spec_name_id)
        
        if email:
            # Generate a random password
            password = generate_random_password()

            # Create a new user (staff member)
            data = Doctor.objects.create(name=name,email=email,specialization=spec, password=password)
            data.save()
            
            # Send the password to the staff via email
            send_mail(
                'Your Doctor Account Details',
                f'Hello {name},\n\nYour Doctor account has been created. Your password is: {password}\nPlease change it after logging in.',
                'abhishekbinish86@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            messages.success(request, "Doctor member created successfully! The password has been sent to their email.")
            return redirect(admin_home)  # Redirect to admin dashboard or another page
        else:
            messages.error(request, "Please provide email.")
    
    departments=Department.objects.all()
    return render(request, 'admin/register_doc.html',{'departments':departments})





# ----------------------------------------------------token--------------------------------------------------------------------------
def book_appointment(request):
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        age=request.POST['age']
        gender=request.POST['gender']
        phone=request.POST['phone']
        address=request.POST['address']
        appointment_date=request.POST['appointment_date']
        department_id=request.POST['department']
        doctor_id=request.POST['doctor']

        department = Department.objects.get(id=department_id)
        doctor = Doctor.objects.get(id=doctor_id)
        
  
        appointment = Appointment.objects.create(name=name,email=email,phone=phone,address=address,department=department,
                                                 doctor=doctor,appointment_date=appointment_date)
        appointment.save()
    else:
        # Fetch categories and brands to populate dropdowns
        doctor = Doctor.objects.all()
        department = Department.objects.all()
        return render(request, 'user/quick_appointmnet.html', {'doctor': doctor, 'department': department})
        



# def book_appointment(req):
#     if 'shop' in req.session:
#         if req.method == 'POST':
#             product_id = req.POST['pid']
#             name = req.POST['name']
#             description = req.POST['description']
#             gender = req.POST['gender']
#             price = req.POST['price']
#             offer_price = req.POST['offer_price']
#             stock = req.POST['stock']
#             file = req.FILES['image']
#             pro_cat_id = req.POST['pro_cat']  # Get selected category ID (no need to create)
#             pro_bnd_id = req.POST['pro_bnd']  # Get selected brand ID (no need to create)

#             # Fetch the related Category and Brand objects
#             pro_cat = Category.objects.get(id=pro_cat_id)
#             pro_bnd = Brand.objects.get(id=pro_bnd_id)
 

#             product = Product.objects.create(pid=product_id,name=name,dis=description,gender=gender.upper(),
#                                 price=price,offer_price=offer_price,stock=stock,img=file,pro_cat=pro_cat,pro_bnd=pro_bnd)

#             product.save()  # Save the product object
#             return redirect(manage_products)
#         else:
#             # Fetch categories and brands to populate dropdowns
#             categories = Category.objects.all()
#             brands = Brand.objects.all()
#             return render(req, 'shop/add_product.html', {'categories': categories, 'brands': brands})
#     else:
#         return redirect(perfume_login)



def get_doctors(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id)
    doctor_list = [{'id': doctor.id, 'name': doctor.name} for doctor in doctors]
    return JsonResponse({'doctors': doctor_list})


def appointment_success(request, token_number):
    return render(request, 'user/appointment_success.html', {'token_number': token_number})













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
