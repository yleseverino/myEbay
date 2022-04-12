from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctions(models.Model):
    product_name = models.CharField(max_length=64)
    description = models.CharField(max_length=4000)
    # categorias
    # img_product = models.ImageField()
    img_product = models.URLField()
    start_bit = models.DecimalField(decimal_places = 2, max_digits = 10)
