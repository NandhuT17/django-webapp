import razorpay # pyright: ignore[reportMissingImports]
from django.shortcuts import render
from .models import Product,Review,Order,OrderItem
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import pycountry

# Create your views here.

def index(request) :
    data = Product.objects.all().order_by('id')

    paginator = Paginator(data,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj' : page_obj,
    }
    return render(request,'products/index.html',context)


def view(request, product_key):
    data = get_object_or_404(Product, pk=product_key)
    if request.method == "POST":
        comment = request.POST.get("comment")

        if comment and request.user.is_authenticated:
            Review.objects.create(
                product=data,
                product_review=comment,
                product_reviewer=request.user
            )
        return redirect('product_view', product_key=product_key)

    reviews = Review.objects.filter(product=data)
    context = {
        "data": data,
        "reviews": reviews,
    }
    return render(request, 'products/view.html', context)


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

    request.session["total"] = float(total) 

    context = {
        'products': products,
        'total': total
    }

    return render(request, 'products/cart.html', context)


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        if cart[str(product_id)] == 1 :
            del cart[str(product_id)]
        else :
            cart[str(product_id)] -= 1

    request.session['cart'] = cart
    return redirect('view_cart')


def buy_now(request,product_key) :
    product = get_object_or_404(Product,id = product_key)
    
    quantity = int(request.GET.get("qty", 1))
    client = razorpay.Client(auth=(settings.TEST_API_KEY,settings.TEST_SECRET_KEY))
    payment = client.order.create({
        'amount': int(product.product_price * quantity * 100),
        'currency': 'INR',
        'payment_capture': 1,
    })

    Order.objects.create(
        razorpay_order_id=payment['id'],
        product=product,
        quantity=quantity
    )

    context = {
        'product' : product,
        'order_id' :payment['id'],
        'razorpay_key' : settings.TEST_API_KEY,
        'amount' : int(product.product_price * quantity * 100),
    }

    return render(request,'products/buy-now.html',context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(
            auth=(settings.TEST_API_KEY, settings.TEST_SECRET_KEY)
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature
            })

            order = Order.objects.get(
                razorpay_order_id=razorpay_order_id
            )

            if not order.is_paid:
                items = OrderItem.objects.filter(order=order)
                if items.exists():
                    # Cart purchase
                    for item in items:
                        product = item.product
                        product.product_stock -= item.quantity
                        product.save()
                else:
                    # Buy Now purchase
                    product = order.product
                    product.product_stock -= order.quantity
                    product.save()

                order.is_paid = True
                order.save()
            return redirect('home')
        
        except Exception as e:
            return HttpResponse(f"Payment Failed {e}")


def checkout(request) :
    total = request.session.get('total',0)
    client = razorpay.Client(auth=(settings.TEST_API_KEY,settings.TEST_SECRET_KEY))
    request.session['email'] = request.user.email
    payment = client.order.create({
        "amount" : int(total*100),
        "currency" : "INR",
        "payment_capture" : 1
    })

    order = Order.objects.create(
        razorpay_order_id=payment['id']
    )
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )

    context = {
        "payment" : payment,
        "razorpay_key" : settings.TEST_API_KEY,
        "total" : total
    }

    return render(request,'products/checkout.html',context)


def search_bar(request) :
    search = request.GET.get('q')

    if search :
        products = Product.objects.filter(
            Q(products_tags__icontains = search) |
            Q(product_name__icontains = search)
        )
    else :
        products = Product.objects.all()

    context = {
        "products" : products,
        "search" : search,
    }
    return render(request,'products/search.html',context)

def delete_review(request,id) :
    review = get_object_or_404(Review,id = id)
    product_id = review.product.id
    if request.user == review.product_reviewer :
        review.delete()
    return redirect('product_view',product_id)


def address(request,product_id) :
    data = Product.objects.get(id=product_id)
    countries = sorted([country.name for country in pycountry.countries])
    context = {
        "data" : data,
        "countries":countries,
    }
    return render(request,"products/address.html",context)