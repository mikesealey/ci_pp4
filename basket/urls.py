from django.urls import path
from .views import add_to_basket, my_basket, remove_from_basket, checkout

urlpatterns = [
    path("add/<int:product_id>/", add_to_basket, name="add_to_basket"),
    path("my_basket/", my_basket, name="my_basket"),
    path("remove/<int:product_id>/", remove_from_basket, name="remove_from_basket"),
    path("checkout/", checkout, name="checkout"),
]