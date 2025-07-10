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

    basket_total = sum(item.product.price * item.qty for item in items)
    shipping_handling = 12 # Shipping and Handling cost
    free_shipping_at = 500 # cost at which shipping becomes free
    difference_to_free_shipping = free_shipping_at - basket_total
    order_total = basket_total
    if order_total < free_shipping_at:
        order_total += shipping_handling

    return render(
        request,
        "basket/my_basket.html",
        {
            "items": items,
            "basket_total": basket_total,
            "shipping_handling": shipping_handling,
            "free_shipping_at": free_shipping_at,
            "difference_to_free_shipping": difference_to_free_shipping,
            "order_total": order_total 
        }
    )

@login_required
def remove_from_basket(request, product_id):
    item = get_object_or_404(
        BasketItem,
        basket__user=request.user,
        product__id=product_id
    )
    item.delete()
    return redirect(request.META.get("HTTP_REFERER", "my_basket"))