from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from basket.views import Address
from allauth.account.views import ConfirmEmailView


def homepage(request):
    return render(request, "base.html")


def my_profile(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    addresses = Address.objects.filter(user=request.user, hidden=False)

    return render(request, "account/profile.html", {
        "orders": orders,
        "addresses": addresses
        })


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "Successfully logged out.")
        return super().get(request, *args, **kwargs)


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.hidden = True
    address.save()
    messages.success(request, "Address deleted.")
    return redirect("my_profile")


class ConfirmEmailAutoLoginView(ConfirmEmailView):
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        self.object.confirm(self.request)
        return redirect('/accounts/login/')