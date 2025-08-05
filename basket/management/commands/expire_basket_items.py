from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from basket.models import BasketItem
from catalogue.models import Product

# New users might not have a wishlist by default as it's created when they add an item to it
try:
    from wishlist.models import WishlistItem, Wishlist
except Exception:
    Wishlist = None
    WishlistItem = None
class Command(BaseCommand):
    help = "Products added to the basket are given a timestamp. When setttings.py > BASKET_RESERVATION_HOURS has passed, if the Product is still in the basket - Restore qty_in_stock level, add the product to wishlist instead, delete basket items."

    def handle(self, *args, **options):
        now = timezone.now()
        expired = BasketItem.objects.filter(remain_in_basket_until__lte=now).select_related("product", "basket__user")

        if not expired.exists():
            self.stdout.write("No expired items found.")
            return

        processed = 0
        for item in expired:
            product = item.product
            user = getattr(item.basket, "user", None)
            # Restore qty_in_stock
            product.qty_in_stock += item.qty
            product.save()

            if WishlistItem and Wishlist and user and getattr(user, "is_authenticated", False):
                try:
                    wishlist, _ = Wishlist.objects.get_or_create(user=user)
                    WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
                except Exception as e:
                    error_msg = f"Failed to add product (id={product.id}) to wishlist for user (id={user.id}): {e}"
                    self.stderr.write(error_msg)

            item.delete()
            processed += 1

        self.stdout.write(f"Processed {processed} expired item(s).")