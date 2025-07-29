from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    material = models.CharField(max_length=100)
    finish = models.CharField(max_length=100)
    qty_in_stock = models.PositiveIntegerField()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')