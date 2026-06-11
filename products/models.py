from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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
    product_image = CloudinaryField(
        'image',
        folder = 'products/',
        null=True,
        blank=True
    )
    products_tags = models.CharField(max_length = 200,blank = True)

    def __str__(self) :
        return str(self.product_name or "Unnamed")

class Review(models.Model) :
    product = models.ForeignKey(Product,on_delete=models.CASCADE, null=True, blank=True)
    product_reviewer = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    product_review = models.TextField()


    def __str__(self) :
        return str(self.product_reviewer or "Unknown")
    

class Order(models.Model):
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.razorpay_order_id
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity}"