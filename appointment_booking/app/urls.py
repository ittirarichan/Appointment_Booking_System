from django.urls import path
from . import views

urlpatterns=[
    path('',views.appointment_login),
    path('user_home',views.user_home),
    path('admin_home',views.admin_home),
    path('we',views.user_register),
    path('doctor',views.doc_home),
    path('staff',views.staff_home),
    path('logout',views.logout),
    path('department',views.add_Specialization),
    path('delete_Specialization/<int:id>/', views.delete_Specialization, name='delete_Specialization'),
    # path('register-staff/', views.register_staff, name='register_staff'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    path('services',views.user_services),

    # URL for creating a token
    path('appointment',views.book_appointment),
    path('appointment_success', views.appointment_success, name='appointment_success'),
    path('get-doctors/',views.get_doctors, name='get_doctors'),
    path('doctor_appointments_view',views.doctor_appointments_view),
    path('patient/<int:patient_id>/details/', views.view_patient_details, name='view_patient_details'),
    path('prescribe/<int:patient_id>/', views.view_patient_details, name='prescribe_medication'),
]