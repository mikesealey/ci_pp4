from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models import Product
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem

# Create your views here.
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    item, created = WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product,
        defaults={"qty": 1}
    )

    if not created:
        item.qty += 1
        item.save()

    return redirect("products_list") # Should figure out some toast notificaiton instead of leaving the page

@login_required
def my_wishlist(request):
    wishlist = getattr(request.user, "wishlist", None)
    items = wishlist.items.select_related("product") if wishlist else []
    return render(request, "wishlist/my_wishlist.html", {"items": items})