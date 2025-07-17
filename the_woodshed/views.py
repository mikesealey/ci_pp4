from django.shortcuts import render
from catalogue.models import Product
from django.contrib.auth.decorators import login_required
from orders.models import Order

def homepage(request):
    return render(request, "base.html")

def products_list(request):
    category = request.GET.get("category")
    if category:
        products = Product.objects.filter(category__iexact=category)
    else:
        products = Product.objects.all()
    return render(request, "products/products_list.html", {"products": products})

def product_search(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__iexact=category)

    return render(request, "products/products_list.html", {
        "products": products
    })

def my_profile(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "account/profile.html", {"orders": orders})

@login_required
def my_past_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, "account/past_orders.html", {"orders": orders})


