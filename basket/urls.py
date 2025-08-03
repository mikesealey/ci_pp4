from django.urls import path
from .views import add_to_basket, my_basket, remove_from_basket, checkout, create_payment_intent, payment_success, payment_error, update_basket_item_qty

urlpatterns = [
    path("add/<int:product_id>/", add_to_basket, name="add_to_basket"),
    path("my_basket/", my_basket, name="my_basket"),
    path("remove/<int:product_id>/", remove_from_basket, name="remove_from_basket"),
    path("checkout/", checkout, name="checkout"),
    path("checkout/payment-intent/", create_payment_intent, name="create_payment_intent"),
    path("success/", payment_success, name="payment_success"),
    path("error/", payment_error, name="payment_error"),
    path("update-item/", update_basket_item_qty, name="update_basket_item_qty"),
]