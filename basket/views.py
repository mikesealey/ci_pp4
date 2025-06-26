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

    return redirect("products_list") # Should figure out some toast notificaiton instead of leaving the page
