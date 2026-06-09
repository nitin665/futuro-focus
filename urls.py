from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('home/', views.homepage, name='homepage'),
    path('enroll/', views.enroll, name='enroll'),
    path('course/', views.course, name='course'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
path('resend-otp/', views.resend_otp, name='resend_otp'),
]