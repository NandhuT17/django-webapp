from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from dashboard.models import Brand

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
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    product_price = models.IntegerField()
    product_category = models.CharField(
        max_length=30,
        choices=CategoryChoice.choices,
        default=CategoryChoice.OTHERS
    )
    product_stock = models.IntegerField(default=0)
    product_desc = models.TextField(max_length=800)
    product_image = CloudinaryField(
        'image',
        folder = 'products/',
        null=True,
        blank=True
    )



class Review(models.Model) :
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    product_reviewer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    product_review = models.TextField()
