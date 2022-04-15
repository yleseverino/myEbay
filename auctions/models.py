from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class auctions(models.Model):
    product_name = models.CharField(max_length=64)
    description = models.CharField(max_length=4000)
    # categorias
    # img_product = models.ImageField()
    img_product = models.URLField()
    start_bit = models.DecimalField(decimal_places = 2, max_digits = 10)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.product_name}"

class Bids(models.Model):
    product = models.ForeignKey(auctions, on_delete=models.CASCADE, related_name="bids")
    bid = models.DecimalField(decimal_places = 2, max_digits = 10)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.product} : {self.bid} at {self.timestamp.strftime('%d/%m/%Y : %H:%M')}"

class Comments(models.Model):
    product = models.ForeignKey(auctions, on_delete=models.CASCADE)
    comment = models.CharField(max_length=4000)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return f"({self.product}) {self.comment} "
