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

def basket_item_count(request):
    # Want to allow anon checkout in future, but for now this must be authenticcated per user
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).first()
        count = basket.items.aggregate(total_qty=models.Sum('qty'))['total_qty'] or 0
    else:
        count = 0
    return {"basket_item_count": count}