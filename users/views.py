from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


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
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = email,
                email = email,
                password = password1,
            )
            login(request,user)
            messages.success(request,"You are logged in successfully")
            return redirect('home')
        
    return render(request,'users/register.html')


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


