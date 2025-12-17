from typing import List

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Location(models.Model):
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"Miсто: {self.location}"


class Subscription(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    locations = models.ManyToManyField(Location)
    services = models.CharField(max_length=50,default="")

    def __str__(self):
        return f"Підписка: {self.name} за {self.price}, послуги: {self.services}"

class Service(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    ipv_4_ext = models.GenericIPAddressField(unique=True,null=True, blank=True,default=None)
    price_per_month_4_ext = models.FloatField(default=0)
    ipv_4_local = models.GenericIPAddressField(unique=True,null=True, blank=True,default=None)
    price_per_month_4_local = models.FloatField(default=0)
    ipv_6 = models.GenericIPAddressField(unique=True,null=True, blank=True,default=None)
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE)