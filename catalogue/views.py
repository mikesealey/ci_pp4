from django.shortcuts import render, get_object_or_404
from .models import Product


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
