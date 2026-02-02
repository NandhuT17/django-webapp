from django.shortcuts import render,redirect
from products.models import Product
from .forms import ProductForm
# Create your views here.


def admin_dashboard(request) :
    data = Product.objects.order_by('?')[:6]
    context = {
        "data" : data,
    }
    return render(request,'dashboard/admin-dashboard.html',context)



def product_details(request,product_key) :
    data = Product.objects.get(pk=product_key)
    context = {
        "data" : data,
    }
    return render(request,'dashboard/product-details.html',context)

def manage_products(request,product_key) :
    data = Product.objects.get(pk=product_key)
    form = ProductForm(request.POST or None , instance=data)
    if form.is_valid() :
        form.save()
        return redirect('product_details')
    
    context = {
        "form" : form,
    }
    return render(request,'dashboard/manage-products.html',context)


