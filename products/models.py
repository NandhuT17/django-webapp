from django.db import models

# Create your models here.

class Product(models.Model) :

    class CategoryChoice(models.TextChoices) :
        electonics = "Electronics","Electronics"
        fashion = "Fashion","Fashion"
        grocery = "Grocery","Grocery"
        others = "Others","Others"

    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField()
    product_category = models.CharField(choices=CategoryChoice.choices,default="Others")
    product_desc = models.TextField(max_length=800)
    product_image = models.CharField(max_length=255,default="https://support.ptc.com/help/thingworx/platform/r9/en/ThingWorx/images/ImageWidgetBeta.png")

    