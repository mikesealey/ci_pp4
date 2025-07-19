from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models import Product
from django.contrib.auth.decorators import login_required
from .models import Wishlist, WishlistItem
from django.contrib import messages

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

    message = "Added item to wishlist" # Want to add product name here later
    messages.success(request, message)
    return redirect(request.META.get("HTTP_REFERER", "products_list"))

@login_required
def my_wishlist(request):
    wishlist = getattr(request.user, "wishlist", None)
    items = wishlist.items.select_related("product") if wishlist else []
    return render(request, "wishlist/my_wishlist.html", {"items": items})

@login_required
def remove_from_wishlist(request, product_id):
    item = get_object_or_404(
        WishlistItem,
        wishlist__user=request.user,
        product__id=product_id
    )
    item.delete()
    return redirect("my_wishlist")