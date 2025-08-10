from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.products_list, name="products_list"),
    path('search', views.product_search, name="product_search"),
    path("<int:pk>/", views.product_detail, name="product_detail"),
]
