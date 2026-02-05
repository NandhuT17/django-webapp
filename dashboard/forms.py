from products.models import Product
from django import forms


class ProductForm(forms.ModelForm) :
    class Meta :
        model = Product
        fields = [
            "product_name",
            "product_price",
            "product_category",
            "product_stock",
            "product_desc",
            "product_image",

        ]