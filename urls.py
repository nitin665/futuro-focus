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
path('login/', views.login_user, name='login'),
path('logout/', views.logout_user, name='logout'),
path('forgot-password/send-otp/', views.forgot_password_send_otp, name='forgot_password_send_otp'),
path('forgot-password/verify-otp/', views.forgot_password_verify_otp, name='forgot_password_verify_otp'),
path('forgot-password/reset/', views.forgot_password_reset, name='forgot_password_reset'),
]