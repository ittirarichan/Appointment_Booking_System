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
    path('register-staff/', views.register_staff, name='register_staff'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),
    path('services',views.user_services),

    ]