from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('view/<int:product_key>/',views.view,name="product_view"),
    path('category',views.category_filter,name="category"),
    path('category/<str:cat_name>',views.category_filter,name="cat_filter"),
]