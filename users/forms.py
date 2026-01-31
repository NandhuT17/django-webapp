from django import forms
from base.models import Product


class Product_Form(forms.ModelForm):
    class Meta :
        model = Product
        fields =[
            'product_name',
            'product_price',
            'product_category',
            'product_desc',
            'product_image',
            ]