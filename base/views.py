from django.shortcuts import render
from .models import Product
# Create your views here.

def index(request) :
    data = Product.objects.all()
    context = {
        "data" : data,
    }
    return render(request,'base/index.html',context)