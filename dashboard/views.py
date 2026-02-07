from django.shortcuts import render,redirect
from products.models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail

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
