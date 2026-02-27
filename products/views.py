from django.shortcuts import render
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
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