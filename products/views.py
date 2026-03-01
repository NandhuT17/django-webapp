import razorpay # pyright: ignore[reportMissingImports]
from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
        "selected_category" : selected_category ,
    }
    return render(request,'products/category.html',context)



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        product.total_price = product.product_price * quantity
        product.quantity = quantity
        total += product.total_price
        products.append(product)

    context = {
        'products': products,
        'total': total
    }

    return render(request, 'products/cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('view_cart')

def buy_now(request,product_key) :
    product = get_object_or_404(Product,id = product_key)

    client = razorpay.Client(auth=(settings.TEST_API_KEY,settings.TEST_KEY_SECRET))

    payment = client.order.create({
        'amount' : int(product.product_price * 100),
        'currency' : 'INR',
        'payment_capture' : '1',
    })

    context = {
        'product' : product,
        'order_id' :payment['id'],
        'razorpay_key' : settings.TEST_API_KEY,
        'amount' : int(product.product_price*100),
    }

    return render(request,'products/buy-now.html',context)



@csrf_exempt
def payment_success(request):

    if request.method == "POST":

        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(auth=(settings.TEST_API_KEY, settings.TEST_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

            return redirect('home')
            return HttpResponse("Payment Successful")
        except:
            return HttpResponse("Payment Failed")