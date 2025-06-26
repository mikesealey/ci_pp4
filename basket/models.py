from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Product

# Create your models here.
class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="basket")

class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)