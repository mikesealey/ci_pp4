from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Product
from django.conf import settings


class Address(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="addresses"
        )
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    town_city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.address1}, {self.town_city}"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
        )
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return sum(item.subtotal() for item in self.items.all())

    def total(self):
        subtotal = self.subtotal()
        if subtotal < settings.FREE_SHIPPING_AT:
            return subtotal + settings.SHIPPING_HANDLING
        return subtotal

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
        )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.qty * self.price
