from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models import Product
from django.contrib.auth.decorators import login_required
from .models import Basket, BasketItem

# Create your views here.
@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    basket, _ = Basket.objects.get_or_create(user=request.user)

    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={"qty": 1}
    )

    if not created:
        item.qty += 1
        item.save()

    return redirect(request.META.get("HTTP_REFERER", "products_list"))

@login_required
def my_basket(request):
    basket = getattr(request.user, "basket", None)
    items = basket.items.select_related("product") if basket else []
    return render(request, "basket/my_basket.html", {"items": items})

@login_required
def remove_from_basket(request, product_id):
    item = get_object_or_404(
        BasketItem,
        basket__user=request.user,
        product__id=product_id
    )
    item.delete()
    return redirect(request.META.get("HTTP_REFERER", "my_basket"))