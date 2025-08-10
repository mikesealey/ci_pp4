from django.test import TestCase, Client
from basket.models import Basket, BasketItem
from django.contrib.auth.models import User
from catalogue.models import Product
from django.urls import reverse


class BasketTests(TestCase):
    # In the current version of The Woodshed - adding products to wishlist
    # or basket can only be done as a logged in user
    def setUp(self):
        # Creates a user and product
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="pass"
            )
        self.product = Product.objects.create(
            name="Test Product",
            price=50,
            qty_in_stock=5,
            category="Furniture"
        )

    def login(self):
        # Logs user in
        self.client.login(username="testuser", password="pass")

    def test_add_to_basket_creates_basket_and_item(self):
        # Add one item - item quantity should be 1
        self.login()
        response = self.client.get(reverse(
            "add_to_basket",
            args=[self.product.id]
            ))
        self.assertRedirects(response, reverse("products_list"))
        basket = Basket.objects.get(user=self.user)
        item = basket.items.get(product=self.product)
        self.assertEqual(item.qty, 1)

    def test_add_to_basket_increments_qty(self):
        # Add two items - item quantity should be 2
        self.login()
        self.client.get(reverse("add_to_basket", args=[self.product.id]))
        self.client.get(reverse("add_to_basket", args=[self.product.id]))
        item = Basket.objects.get(user=self.user).items.get(
            product=self.product
            )
        self.assertEqual(item.qty, 2)

    def test_remove_from_basket(self):
        # Create a basket with an item, remove the item, check if it exists
        self.login()
        basket = Basket.objects.create(user=self.user)
        BasketItem.objects.create(basket=basket, product=self.product, qty=1)
        response = self.client.get(reverse(
            "remove_from_basket",
            args=[self.product.id]
            ))
        self.assertRedirects(response, reverse("my_basket"))
        self.assertFalse(BasketItem.objects.filter(basket=basket).exists())
