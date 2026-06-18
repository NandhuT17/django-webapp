from django.db import models
from django.conf import settings
# Create your models here.

class Address(models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE,)
    country = models.CharField(max_length=100)
    fullname = models.CharField(max_length=150)
    mobilenumber = models.IntegerField()
    flat_no = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    pincode = models.IntegerField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)