from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):

    class CategoryChoice(models.TextChoices):
        BEVERAGES = "Beverages", "Beverages"
        ELECTRONICS = "Electronics", "Electronics"
        FASHION = "Fashion", "Fashion"
        GROCERY = "Grocery", "Grocery"
        PERSONAL_CARE = "Personal Care", "Personal Care"
        SNACKS = "Snacks", "Snacks"
        STATIONARY = "Stationary", "Stationary"
        OTHERS = "Others", "Others"

    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_category = models.CharField(
        max_length=30,
        choices=CategoryChoice.choices,
        default=CategoryChoice.OTHERS
    )
    product_stock = models.IntegerField(default=0)
    product_desc = models.TextField(max_length=800)
    product_image = models.CharField(
        max_length=255,
        default="https://support.ptc.com/help/thingworx/platform/r9/en/ThingWorx/images/ImageWidgetBeta.png"
    )




    