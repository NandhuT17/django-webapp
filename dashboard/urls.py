from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('superuser',views.admin_dashboard,name="superlogin"),
    path('product-details/<int:product_key>',views.product_details,name="product_details"),
    path('manage-products/<int:product_key>',views.manage_products,name="manage"),
    path('add-products',views.add_products,name="add-products"),
    
]