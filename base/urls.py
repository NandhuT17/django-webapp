from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name="home"),
    path('view/<int:product_key>/',views.view,name="product_view"),
]