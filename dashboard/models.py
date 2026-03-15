from django.db import models
from products.models import User
# Create your models here.

class Store(models.Model) :
    name = models.CharField(max_length=100)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) :
        return self.name