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
    product_image = models.CharField(max_length=255,default="https://media.istockphoto.com/id/2149660186/vector/no-photo-thumbnail-graphic-element-no-found-or-available-image-in-the-gallery-or-album-flat.jpg?s=170667a&w=0&k=20&c=6OxmlrwylptcDddq_WfpJX3L8wo00DULS29JK7MFZWY=")

    