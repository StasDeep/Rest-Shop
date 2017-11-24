from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from restshop.api.product.models import Product
from restshop.api.unit.models import Unit
from restshop.api.user.models import Seller


class OrderTestCase(APITestCase):
    order_data = {
        'name': 'Temp',
        'phone': '+375555555',
        'address': '5th Str 55'
    }

    def setUp(self):
        self.order_url = reverse('restshop:order-list')
        self.cart_url = reverse('restshop:cart')

        User.objects.create_user('temp', 'temp@gmail.com', '123123')
        self.client.login(username='temp', password='123123')

        seller_user = User.objects.create_user('nike', 'nike@gmail.com', '123123')
        seller = Seller.objects.create(user=seller_user, name='Nike', address='California')

        product = Product.objects.create(seller=seller, title='Nike Huarache')
        Unit.objects.create(product=product, sku='000000', price=95, num_in_stock=10)
        Unit.objects.create(product=product, sku='000001', price=95, num_in_stock=10)

        seller_user = User.objects.create_user('adidas', 'adidas@gmail.com', '123123')
        seller = Seller.objects.create(user=seller_user, name='Adidas', address='California')

        product = Product.objects.create(seller=seller, title='Adidas Yeezy Boost')
        Unit.objects.create(product=product, sku='100000', price=95, num_in_stock=10)
        Unit.objects.create(product=product, sku='100001', price=95, num_in_stock=10)
        Unit.objects.create(product=product, sku='100002', price=95, num_in_stock=0)

    def add_to_cart_and_assert(self, unit=None, expected_status=status.HTTP_201_CREATED):
        """Add to cart and check if response has the same status as expected."""
        if unit is None:
            unit = {'sku': '000000', 'quantity': 2}

        response = self.client.post(self.cart_url, unit)
        self.assertEqual(response.status_code, expected_status)

    def assert_cart_length(self, expected_length, quantity_of=None):
        """Check cart length and, if passed, quantity of the item.
        quantity_of is a 2-item tuple where quantity_of[0] is the index of item
                                        and quantity_of[1] is the expected quantity."""
        response = self.client.get(self.cart_url)
        self.assertEqual(len(response.data['data']), expected_length)

        if quantity_of is not None:
            self.assertEqual(response.data['data'][quantity_of[0]]['quantity'], quantity_of[1])

        return response

    def order_and_assert(self, data=None, expected_status=status.HTTP_201_CREATED):
        if data is None:
            data = self.order_data

        response = self.client.post(self.order_url, data)
        self.assertEqual(response.status_code, expected_status)

    def assert_orders_length(self, expected_length):
        response = self.client.get(self.order_url)
        self.assertEqual(len(response.data['data']), expected_length)

    def test_add_to_cart(self):
        """Test adding to cart by a common user."""
        self.add_to_cart_and_assert()
        self.assert_cart_length(1)

    def test_add_same_unit(self):
        """Test adding to cart the same unit.
        Cart should not change the number of elements.
        But quantity should be updated if passed."""
        self.add_to_cart_and_assert({'sku': '000000'})
        self.assert_cart_length(1, quantity_of=(0, 1))

        self.add_to_cart_and_assert({'sku': '000000', 'quantity': 2})
        self.assert_cart_length(1, quantity_of=(0, 2))

    def test_add_nonexistent_unit(self):
        """Test adding a nonexistent unit to cart."""
        self.add_to_cart_and_assert({'sku': '999'}, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_add_too_many_items(self):
        """Test adding more items of unit than available."""
        self.add_to_cart_and_assert({'sku': '000000', 'quantity': 15},
                                    expected_status=status.HTTP_400_BAD_REQUEST)

    def test_add_to_cart_anonymously(self):
        """Test adding unit to cart not being logged in."""
        self.client.logout()
        self.add_to_cart_and_assert()
        self.assert_cart_length(1)

    def test_order(self):
        """Test creating order as a common user."""
        self.add_to_cart_and_assert()
        self.order_and_assert()
        self.assert_orders_length(1)

    def test_order_with_empty_cart(self):
        """Test creating order with no units in cart."""
        self.order_and_assert(expected_status=status.HTTP_400_BAD_REQUEST)
        self.assert_orders_length(0)

    def test_order_anonymously(self):
        """Test order not being logged in."""
        self.client.logout()
        self.add_to_cart_and_assert()
        self.order_and_assert()


class UserTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('restshop:auth')
        User.objects.create_user('temp', 'temp@gmail.com', '123123')

    def test_login(self):
        """Log in as a common user."""
        response = self.client.post(self.url, {'username': 'temp', 'password': '123123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('restshop:order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

        response = self.client.get(reverse('restshop:order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """Log out as a common user."""
        response = self.client.post(self.url, {'username': 'temp', 'password': '123123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('restshop:order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.delete(self.url)

        response = self.client.get(reverse('restshop:order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
