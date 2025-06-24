from django.urls import path
from .views import add_to_wishlist, my_wishlist

urlpatterns = [
    path("add/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("my_wishlist/", my_wishlist, name="my_wishlist"),
]