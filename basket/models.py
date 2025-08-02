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
    """
    Returns a dictionary with the total quantity of items in the 
    authenticated user's basket, or zero if the user is not logged in 
    or has no basket. (A basket is only created when a new user adds their first product)
    """
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).first()
        if basket:
            count = basket.items.aggregate(total_qty=models.Sum('qty'))['total_qty'] or 0
            return {"basket_item_count": count}
    return {"basket_item_count": 0}