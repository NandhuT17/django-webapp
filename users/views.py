from .forms import Product_Form
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from base.models import Product

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
                return redirect('superlogin')
            elif user.is_staff :
                return redirect("stafflogin")
            else :
                return redirect('home')
        else :
            messages.error(request,"Invalid Credentials")
            return redirect('login')
    return render(request,'users/login.html')

def logout_user(request) :
    logout(request)
    return redirect('home')


def admin_dashboard(request) :
    data = Product.objects.all()
    context = {
        "data" : data,
    }
    return render(request,'users/admin-dashboard.html',context)



def product_details(request,product_key) :
    data = Product.objects.get(pk=product_key)
    context = {
        "data" : data,
    }
    return render(request,'users/product-details.html',context)


def edit_products(request,product_key) :
    data = Product.objects.get(pk=product_key)
    form = Product_Form(request.POST or None, instance=data)
    if form.is_valid() :
        form.save()
        return redirect('details')
    context = {
        "form" : form,
    }
    return render(request,'users/edit-products.html',context)