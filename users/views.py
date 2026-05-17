from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.



def register_user(request) :
    if request.method == "POST" :
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1!=password2:
            messages.error(request,"The passwords doesn't match")
            return redirect('register')
        
    
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('register')
        else :
            otp = str(random.randint(1000,9999))
            

            request.session['otp'] = otp
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name
            request.session['email'] = email
            request.session['password'] = password1

            try :
                send_mail(
                    subject = "OTP",
                    message = "Your OTP is " + otp,
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [email],
                )
            except Exception as e :
                print("MAIL ERROR", repr(e))
                raise
            return redirect('otp_verification')
    return render(request,'users/register.html')


def verify_otp(request) :
    if request.method == "POST" :
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp :
            user = User.objects.create_user(
                first_name = request.session['first_name'],
                last_name = request.session['last_name'],
                username = request.session['first_name'] + request.session['last_name'],
                email = request.session['email'],
                password = request.session['password']
            )

            request.session.flush()
            login(request,user)
            

            return redirect('home')
        
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'users/otp_conf.html')


def login_user(request) :
    if request.method == "POST" :
        email = request.POST['email']
        password = request.POST['password']

        try :
            user = User.objects.get(email=email)
        except User.DoesNotExist :
            messages.error(request,"User doesnot exists")
            return redirect('register')
        
        user_details = authenticate(request,username = user.username , password = password)

        if user_details is not None :
            login(request,user_details)

            if user_details.is_superuser :
                return redirect('dashboard:superlogin')
            elif user_details.is_staff :
                return redirect('dashboard:stafflogin')
            else :
                return redirect('home')
        else :
            messages.error(request,"Incorrect password")
            return redirect('login')
    return render(request,'users/login.html')

@login_required
def logout_user(request) :
    logout(request)
    return redirect('login')


