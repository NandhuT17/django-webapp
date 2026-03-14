from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('superuser',views.admin_dashboard,name="superlogin"),
    path('product-details/<int:product_key>',views.product_details,name="product_details"),
    path('manage-products/<int:product_key>',views.manage_products,name="manage"),
    path('add-products',views.add_products,name="add-products"),
    path('delete/<int:product_key>',views.delete_products,name="delete-products"),
    path('contact',views.contact_us,name="contact_us"),
    path('staff',views.admin_dashboard,name="stafflogin"),
    path('statistics/',views.statistics,name="statistics"),
    path('users_details/',views.users_details,name="users_details"),
    path('admin-details/',views.admin_details,name="admin-details"),
    path('staffs-details/',views.staff_details,name="staffs-details"),
    path('prod-details/',views.prod_details,name="prod-details"),
]