from django.shortcuts import render
from catalogue.models import Product

def homepage(request):
    return render(request, "base.html")

def products_list(request):
    products = Product.objects.all()
    return render(request, "products/products_list.html", {"products": products})