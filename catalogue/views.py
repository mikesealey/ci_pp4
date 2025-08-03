from django.shortcuts import render, get_object_or_404
from .models import Product
from django.db.models import Q


# Create your views here.
def products_list(request):
    products = Product.objects.all()
    return render(request, "products_list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/product_details.html", {"product": product})

def product_search(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category__iexact=category)

    return render(request, "products/search_results.html", {"products": products, "query": query, "category": category})

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