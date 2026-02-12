from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.



def register_user(request) :
    if request.method == "POST" :
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1!=password2:
            messages.error(request,"The passwords doesn't match")
            return redirect('register')
        
        user = User.objects.create_user(
            username,
            email,
            password1,
        )
        login(request,user)
        messages.success(request,"You are logged in successfully")
        return redirect('home')
    return render(request,'users/register.html')


def login_user(request) :
    if request.method == "POST" :
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None :
            login(request,user)
            if user.is_superuser :
                return redirect('dashboard:superlogin')
            elif user.is_staff :
                return redirect("dashboard:stafflogin")
            else :
                return redirect('home')
        else :
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request,'users/login.html')

@login_required
def logout_user(request) :
    logout(request)
    return redirect('login')
