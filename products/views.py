from django.shortcuts import render
from .models import Product
# Create your views here.

def index(request) :
    data = Product.objects.order_by('?')[:4]
    context = {
        "data" : data,
    }
    return render(request,'products/index.html',context)

def view(request,product_key) :
    data = Product.objects.get(pk=product_key)
    context = {
        "data" : data,
    }
    return render(request,'products/view.html',context)

