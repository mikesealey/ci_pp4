from django.urls import path
from . import views

urlpatterns = [
    path("my-orders/", views.my_past_orders, name="my_past_orders"),
]
