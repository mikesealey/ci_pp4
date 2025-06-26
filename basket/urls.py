from django.urls import path
from .views import add_to_basket

urlpatterns = [
    path("add/<int:product_id>/", add_to_basket, name="add_to_basket"),
]