from django.urls import path
from . import views

urlpatterns=[
    path('',views.appointment_login),
    path('user_home',views.user_home),
    path('doctor',views.doc_home),
    path('staff',views.staff_home),
    ]