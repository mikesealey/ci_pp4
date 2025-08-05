from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from django.db.models import F
from basket.models import BasketItem
from catalogue.models import Product

# New users might not have a wishlist by default as it's created when they add an item to it
try:
    from wishlist.models import WishlistItem
except Exception:
    WishlistItem = None

class Command(BaseCommand):
    help = "Products added to the basket are given a timestamp. When setttings.py > BASKET_RESERVATION_HOURS has passed, if the Product is still in the basket - Restore qty_in_stock level, add the product to wishlist instead, delete basket items."

    def handle(self, *args, **options):
        now = timezone.now()
        expired = BasketItem.objects.filter(reserved_until__lte=now).select_related("product", "basket__user")

        if not expired.exists():
            self.stdout.write("No expired items found.")
            return

        processed = 0
        for item in expired:
            product = item.product
            user = getattr(item.basket, "user", None)

            product.qty_in_stock = product.qty_in_stock + item.qty
            product.save()

            if WishlistItem and user and getattr(user, "is_authenticated", False):
                try:
                    WishlistItem.objects.get_or_create(user=user, product=product)
                except Exception:
                    pass

            item.delete()
            processed += 1

        self.stdout.write(f"Processed {processed} expired item(s).")