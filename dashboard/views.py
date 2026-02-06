from django.shortcuts import render,redirect
from products.models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def admin_dashboard(request) :
    data = Product.objects.order_by('?')[1:]
    context = {
        "data" : data,
    }
    return render(request,'dashboard/admin-dashboard.html',context)


@login_required
def product_details(request,product_key) :
    data = Product.objects.get(pk=product_key)
    context = {
        "data" : data,
    }
    return render(request,'products/view.html',context)

@login_required
def manage_products(request,product_key) :
    data = Product.objects.get(pk=product_key)
    form = ProductForm(request.POST or None , instance=data)
    if form.is_valid() :
        form.save()
        return redirect('dashboard:product_details',product_key=data.pk)
    
    context = {
        "form" : form,
    }
    return render(request,'dashboard/manage-products.html',context)

@login_required
def add_products(request) :
    form = ProductForm(request.POST or None)
    if form.is_valid() :
        form.save()
        return redirect('home')
    
    context = {
        "form" : form,
    }
    return render(request,'dashboard/add-products.html',context)

@login_required
def delete_products(request,product_key) :
    data = Product.objects.get(pk=product_key)
    if request.method == "POST" :
        data.delete()
        return redirect('home')
    return render(request,'dashboard/delete-product.html')