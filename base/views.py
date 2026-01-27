from django.shortcuts import render
from .models import Product
# Create your views here.

def index(request) :
    data = Product.objects.all()
    context = {
        "data" : data,
    }
    return render(request,'base/index.html',context)

def view(request,product_key) :
    data = Product.objects.get(pk=product_key)
    context = {
        "data" : data,
    }
    return render(request,'base/view.html',context)


def login(request) :
    return render(request,'registration/login.html')