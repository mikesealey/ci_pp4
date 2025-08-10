from django.shortcuts import render
from orders.models import Order
from django.contrib.auth.decorators import login_required


@login_required
def my_past_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    for order in orders:
        order.total = sum(item.subtotal() for item in order.items.all())
    return render(
        request,
        "my_past_orders.html",
        {"orders": orders}
        )
