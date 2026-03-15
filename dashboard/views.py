from django.shortcuts import render,redirect
from products.models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from dashboard.models import Store

# Create your views here.


@login_required
def admin_dashboard(request) :
    data = Product.objects.all()

    paginator = Paginator(data,5)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        "page_obj" : page_obj,
    }
    return render(request,'products/index.html',context)


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
    form = ProductForm(request.POST or None, request.FILES or None, instance=data)
    if form.is_valid() :
        form.save()
        return redirect('dashboard:product_details',product_key=data.pk)
    
    context = {
        "form" : form,
    }
    return render(request,'dashboard/manage-products.html',context)



@login_required
def add_products(request) :
    form = ProductForm(request.POST or None, request.FILES or None)
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
        if data.product_image :
            data.product_image.delete(save=False)
            
        data.delete()
        return redirect('home')
    return render(request,'dashboard/delete-product.html')



@login_required
def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("from_name")
        email = request.POST.get("from_mail")
        message = request.POST.get("from_message")

        email_message = EmailMessage(
            subject="New Contact Message",
            body=f"{message}",
            from_email=settings.EMAIL_HOST_USER,  
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email],   
        )

        email_message.send()

        send_mail(
            subject="Thank You for Contacting Us",
            message="We received your message. We will reply soon.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return render(request, "dashboard/contact-us.html", {"success": True})

    return render(request, "dashboard/contact-us.html")



def statistics(request) :
    admin_count = User.objects.filter(is_superuser = True).count()
    users_count = User.objects.filter(is_superuser = False, is_staff = False).count()
    staff_count = User.objects.filter(is_superuser = False, is_staff = True).count()
    products_count = Product.objects.count()
    context = {
        "admin_count" : admin_count,
        "users_count" : users_count,
        "staff_count" : staff_count,
        "products_count" : products_count
    }
    return render(request,'dashboard/statistics.html',context)



def users_details(request) :
    users = User.objects.filter(is_superuser = False, is_staff = False)
    context = {
        "users" : users,
    }
    return render(request,'dashboard/users-details.html',context)



def admin_details(request) :
    users = User.objects.filter(is_superuser = True)
    context = {
        "users" : users,
    }
    return render(request,'dashboard/admin-details.html',context)



def staff_details(request) :
    users = User.objects.filter(is_superuser = False, is_staff = True)
    context = {
        "users" : users,
    }
    return render(request,'dashboard/staffs-details.html',context)



def prod_details(request) : 
    products = Product.objects.all()
    context = {
        "products" : products,
    }
    return render(request,'dashboard/prod-details.html',context)



def staff_dashboard(request) :
    store = Store.objects.filter(seller = request.user).first()
    products = Product.objects.filter(products_seller = store)

    context = {
        "products" : products,
    }
    return render(request,'dashboard/staff-dashboard.html',context)