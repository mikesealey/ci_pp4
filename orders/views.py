from django.shortcuts import render
from orders.models import Order
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def my_past_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, "my_past_orders.html", {"orders": orders})
