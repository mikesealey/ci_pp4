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
from django.core.mail import send_mail
import os
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.utils.timezone import now

stripe.api_key = settings.STRIPE_SECRET_KEY

shipping_handling = 12  # Shipping and Handling cost
free_shipping_at = 500  # cost at which shipping becomes free


@login_required
def add_to_basket(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    basket, _ = Basket.objects.get_or_create(user=request.user)

    item, created = BasketItem.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={"qty": 1}
    )

    now = timezone.now()
    hours = getattr(settings, "BASKET_RESERVATION_HOURS", 3)

    if not created:
        new_qty = item.qty + 1
        if new_qty > product.qty_in_stock:
            messages.error(
                request,
                f"Cannot add another {product.name} — only "
                f"{product.qty_in_stock} in stock."
            )
        else:
            item.qty = new_qty
            item.added_to_basket_at = now
            item.remain_in_basket_until = now + timezone.timedelta(hours=hours)
            item.save()

            product.qty_in_stock -= 1
            product.save()

            messages.success(request, f"Added {product.name} to basket")
    else:
        product.qty_in_stock -= 1
        product.save()

        item.added_to_basket_at = now
        item.remain_in_basket_until = now + timezone.timedelta(hours=hours)
        item.save()

        messages.success(request, f"Added {product.name} to basket")

    return redirect(request.META.get("HTTP_REFERER", "products_list"))


@login_required
def my_basket(request):
    basket = getattr(request.user, "basket", None)
    items = basket.items.select_related("product") if basket else []

    basket_total = sum(item.product.price * item.qty for item in items)
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

    # Replenishes stock level when item is removed from basket
    product = item.product
    product.qty_in_stock += item.qty
    product.save()

    message = f"Removed {item.product.name} from basket"
    item.delete()
    messages.success(request, message)
    return redirect(request.META.get("HTTP_REFERER", "my_basket"))


@login_required
def checkout(request):
    basket = get_object_or_404(
        Basket.objects.prefetch_related("items__product"),
        user=request.user
        )
    items = basket.items.all()
    basket_total = sum(item.product.price * item.qty for item in items)

    saved_addresses = request.user.addresses.filter(hidden=False)

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

        basket = get_object_or_404(
            Basket.objects.prefetch_related("items__product"),
            user=request.user
            )
        basket_total = sum(
            item.product.price * item.qty
            for item in basket.items.all()
            )
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
    address_data = request.session.get("checkout_address")

    if not address_data:
        return render(request, "basket/success.html", {
            "error": "No address information found in session."
        })

    items = list(BasketItem.objects.filter(basket=basket))
    # need to find a way to _only_ save the address if it's new.
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

    create_order_from_basket(request.user, address)

    if basket and items:
        message_body_lines = [
            f"Hi {request.user.first_name or request.user.username},",
            "",
            "Thanks for your purchase from The Wood Shed!",
            "",
            "Your order summary:",
        ]

        for item in items:
            message_body_lines.append(f"- {item.product.name} (x{item.qty})")

        message_body_lines += [
            "",
            f"Shipping to: {address.name}, {address.address1}, "
            f"{address.town_city}, {address.postcode}",
            "",
            f"Order placed on: "
            f"{now().strftime('%d %B %Y at %H:%M')}",
            "",
            "We'll be in touch when your order ships.",
            "",
            "Thanks again,",
            "The Wood Shed Team"
        ]

        send_mail(
            subject="Your Order Confirmation",
            message="\n".join(message_body_lines),
            from_email=os.environ.get("EMAIL_HOST_USER"),
            recipient_list=[request.user.email]
        )

        for item in items:
            product = item.product
            product.qty_in_stock -= item.qty
            product.save()

    messages.success(request, "Success! Your order has been placed")
    return render(request, "basket/success.html")


def payment_error(request):
    message = "An error has occcured. Your card as not been charged"
    messages.error(request, message)
    return render(request, "basket/error.html")


@login_required
@require_POST
@csrf_exempt
def update_basket_item_qty(request):
    data = json.loads(request.body)
    item_id = data.get("item_id")
    new_qty = int(data.get("qty"))

    item = BasketItem.objects.get(id=item_id, basket__user=request.user)

    item.qty = new_qty
    item.save()

    basket = item.basket
    items = basket.items.select_related("product")

    basket_total = sum(i.product.price * i.qty for i in items)
    order_total = (
        basket_total if basket_total >= free_shipping_at
        else basket_total + shipping_handling
    )

    return JsonResponse({
        "status": "ok",
        "basket_total": f"£{basket_total}",
        "order_total": f"£{order_total}"
    })
