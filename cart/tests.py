from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
from .cart import Cart


class CartTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.product = Product.objects.create(
            name='Test Product', price=10.0, image='test.jpg')

    def test_update_cart_increment(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('update_cart', args=[self.product.id, 'increment']))
        self.assertEqual(response.status_code, 200)
        cart = Cart(self.client.session)
        self.assertEqual(cart.get_item(self.product.id)['quantity'], 1)

    def test_update_cart_decrement(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart(self.client.session)
        cart.add(product=self.product, quantity=2)
        response = self.client.get(reverse('update_cart', args=[self.product.id, 'decrement']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(cart.get_item(self.product.id)['quantity'], 1)

    def test_update_cart_remove(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart(self.client.session)
        cart.add(product=self.product, quantity=1)
        response = self.client.get(reverse('update_cart', args=[self.product.id, 'remove']))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(cart.get_item(self.product.id))

    def test_update_cart_clear(self):
        self.client.login(username='testuser', password='testpass')
        cart = Cart(self.client.session)
        cart.add(product=self.product, quantity=1)
        response = self.client.get(reverse('update_cart', args=[self.product.id, 'clear']))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(cart.get_item(self.product.id))