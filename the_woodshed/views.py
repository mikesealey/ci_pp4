from django.shortcuts import render
from catalogue.models import Product
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from basket.views import Address
from django.db.models import Q

def homepage(request):
    return render(request, "base.html")

def products_list(request):
    category = request.GET.get("category")
    hide_out_of_stock = request.GET.get("hide_out_of_stock") == "1"
    sort = request.GET.get("sort")

    products = Product.objects.all()

    if category:
        products = Product.objects.filter(category__iexact=category)

    if hide_out_of_stock:
        products = products.filter(qty_in_stock__gt=0)
    
    if sort == "price_low_high":
        products = products.order_by("price")
    elif sort == "price_high_low":
        products = products.order_by("-price")

    return render(request, "products/products_list.html", {"products": products})

def product_search(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(material__icontains=query) |
            Q(finish__icontains=query)
        )
    if category:
        products = products.filter(category__iexact=category)

    return render(request, "products/products_list.html", {
        "products": products
    })

def my_profile(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    addresses = Address.objects.filter(user=request.user, hidden=False)

    return render(request, "account/profile.html", {"orders": orders, "addresses": addresses})

@login_required
def my_past_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, "account/past_orders.html", {"orders": orders})



class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        return super().get(request, *args, **kwargs)

