from django.shortcuts import render
from .models import Product

# Create your views here.

def index(request) :
    data = Product.objects.order_by('?')[:5]
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

def category_filter(request,cat_name=None) :
    category = Product.CategoryChoice.choices

    products = Product.objects.all()
    selected_category = None

    if cat_name :
        selected_category = cat_name
        products = products.filter(product_category = cat_name)

    context = {
        "category" : category,
        "products" : products,
        "selected_category" :selected_category,
    }
    return render(request,'products/category.html',context)