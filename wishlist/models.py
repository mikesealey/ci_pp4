from django.db import models
from django.contrib.auth.models import User
from catalogue.models import Product


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist"
        )


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name="items"
        )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)


def wishlist_item_count(request):
    # Want to allow anon checkout/wishlist in future, but for now this
    # must be authenticcated per user
    """
    Returns a dictionary with the total quantity of items in the
    authenticated user's wishlist, or zero if the user is not logged in
    or has no wishlist.
    (A wishlist is only created when a new user adds their first product)
    """
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            count = wishlist.items.aggregate(
                total_qty=models.Sum('qty')
                )['total_qty'] or 0
        else:
            count = 0
    else:
        count = 0
    return {"wishlist_item_count": count}
