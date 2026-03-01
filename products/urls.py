from django.urls import path
from . import views
from users.views import create_admin

urlpatterns = [
    path('',views.index,name="home"),
    path('view/<int:product_key>/',views.view,name="product_view"),
    path('category',views.category_filter,name="category"),
    path('category/<str:cat_name>',views.category_filter,name="cat_filter"),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/<int:product_key>',views.buy_now,name="payment-page"),
    path('confirmation/',views.payment_success,name="payment_success"),
    path('create-admin/',create_admin),
]

