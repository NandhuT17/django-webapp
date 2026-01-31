from django.urls import path
from . import views

urlpatterns =[
    path('login',views.login_user,name="login"),
    path('register',views.register_user,name="register"),
    path('logout',views.logout_user,name="logout"),
    path('superlogin',views.admin_dashboard,name="superlogin"),
    path('details/<int:product_key>',views.product_details,name="details"),
    path('edit-product/<int:product_key>',views.edit_products,name="edit")
]