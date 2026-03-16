from django.db import models
from products.models import User
# Create your models here.


class Brand(models.Model) :
    user  = models.OneToOneField(User,on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=100)
    brand_email = models.EmailField()
    
    def __str__(self) :
        return self.brand_name
    
