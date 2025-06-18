from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    material = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    images = models.JSONField()  # JSON will hold an arrya of image-URLS
    qty_in_stock = models.PositiveIntegerField()