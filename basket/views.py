from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models import Product
from django.contrib.auth.decorators import login_required
from .models import Basket, BasketItem
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
import json
from orders.utils import create_order_from_basket
from orders.models import Address
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    message = f"Added {product.name} to basket"
    messages.success(request, message)
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
    message = f"Removed {item.product.name} from basket"
    item.delete()
    print(message)
    messages.success(request, message)
    return redirect(request.META.get("HTTP_REFERER", "my_basket"))

@login_required
def checkout(request):
    basket = get_object_or_404(Basket.objects.prefetch_related("items__product"), user=request.user)
    items = basket.items.all()
    basket_total = sum(item.product.price * item.qty for item in items)

    saved_addresses = request.user.addresses.all()

    return render(request, "basket/checkout.html", {
        "items": items,
        "basket_total": basket_total,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "saved_addresses": saved_addresses
    })

@csrf_exempt
@login_required
def create_payment_intent(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")

    try:
        data = json.loads(request.body)
        shipping = data.get("shipping")

        # Save the address info to the session so /basket/success can use it
        request.session["checkout_address"] = shipping

        basket = get_object_or_404(Basket.objects.prefetch_related("items__product"), user=request.user)
        basket_total = sum(item.product.price * item.qty for item in basket.items.all())
        amount = int(basket_total * 100)  # in pence

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="gbp",
            metadata={"user_id": request.user.id}
        )
        return JsonResponse({"client_secret": intent.client_secret})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@login_required
def payment_success(request):
    basket = Basket.objects.filter(user=request.user).first()
    print("BASKET>>>>>>", basket)

    address_data = request.session.get("checkout_address")

    if not address_data:
        return render(request, "basket/success.html", {
            "error": "No address information found in session."
        })

    address = Address.objects.create(
        user=request.user,
        name=address_data.get("name"),
        address1=address_data.get("address1"),
        address2=address_data.get("address2"),
        town_city=address_data.get("town_city"),
        postcode=address_data.get("postcode"),
        phone=address_data.get("phone"),
        email=address_data.get("email"),
    )
    print("request.user and address", request.user, address)

    create_order_from_basket(request.user, address)

    if basket:
        items = BasketItem.objects.filter(basket=basket)
        for item in items:
            product = item.product
            product.qty_in_stock -= item.qty
            product.save()
        items.delete()

    message = "Succcess! Your order has been placed"
    messages.success(request, message)
    return render(request, "basket/success.html")

def payment_error(request):
    
    message = "An error has occcured. Your card as not been charged"
    messages.error(request, message)
    return render(request, "basket/error.html")


