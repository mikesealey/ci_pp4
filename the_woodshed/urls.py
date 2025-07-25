"""the_woodshed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import homepage, products_list, product_search, my_profile, my_past_orders
from . import views
from catalogue import views
from .views import CustomLogoutView

urlpatterns = [
    path('', homepage, name="homepage" ),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('products/', products_list, name="products_list"),
    path('search', product_search, name="product_search"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("wishlist/", include("wishlist.urls")),
    path("basket/", include("basket.urls")),
    path("profile/", my_profile, name="my_profile"),
    path("profile/orders/", my_past_orders, name="past_orders"),
    path("orders/", include("orders.urls")),
    path("logout/", CustomLogoutView.as_view(next_page="/"), name="logout"),
]
