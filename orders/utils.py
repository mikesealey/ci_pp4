from orders.models import Order, OrderItem
from basket.models import Basket
from django.db import transaction


@transaction.atomic
def create_order_from_basket(user, address):
    basket = Basket.objects.prefetch_related("items__product").get(user=user)

    order = Order.objects.create(
        user=user,
        address=address
    )

    order_items = [
        OrderItem(
            order=order,
            product=item.product,
            qty=item.qty,
            price=item.product.price
        )
        for item in basket.items.all()
    ]

    OrderItem.objects.bulk_create(order_items)

    basket.items.all().delete()

    return order
