from django.urls import path
from . import views

urlpatterns =[
    path('login',views.login_user,name="login"),
    path('verify_otp',views.verify_otp,name="otp_verification"),
    path('register',views.register_user,name="register"),
    path('logout',views.logout_user,name="logout"),
]