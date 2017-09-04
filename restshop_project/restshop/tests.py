from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Order, Product, Seller, Unit, OrderUnit


class OrderTestCase(APITestCase):
    order_data = {
        'name': 'Temp',
        'phone': '+375555555',
        'address': '5th Str 55',
        'units': [
            {'sku': '000000', 'quantity': 2},
            {'sku': '000001', 'quantity': 2}
        ]
    }

    def setUp(self):
        self.url = reverse('restshop:order-list')

        User.objects.create_user('temp', 'temp@gmail.com', '123123')
        self.client.login(username='temp', password='123123')

        seller_user = User.objects.create_user('nike', 'nike@gmail.com', '123123')
        seller = Seller.objects.create(user=seller_user, name='Nike', address='California')

        product = Product.objects.create(seller=seller, title='Nike Huarache')
        Unit.objects.create(product=product, sku='000000', price=95)
        Unit.objects.create(product=product, sku='000001', price=95)

        seller_user = User.objects.create_user('adidas', 'adidas@gmail.com', '123123')
        seller = Seller.objects.create(user=seller_user, name='Adidas', address='California')

        product = Product.objects.create(seller=seller, title='Adidas Yeezy Boost')
        Unit.objects.create(product=product, sku='100000', price=95)
        Unit.objects.create(product=product, sku='100001', price=95)
        Unit.objects.create(product=product, sku='100002', price=95, num_in_stock=0)

    def create_order_and_assert(self, data=None):
        if data is None:
            data = self.order_data

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order(self):
        """Create a new order object."""
        self.create_order_and_assert()
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderUnit.objects.count(), 2)
        self.assertEqual(Unit.objects.get(sku='000000').num_in_stock, 3)

    def test_create_order_different_sellers(self):
        """Create multiple orders by ordering products from different sellers."""
        data = {
            'name': 'Temp',
            'phone': '+375555555',
            'address': '5th Str 55',
            'units': [
                {'sku': '000000', 'quantity': 2},
                {'sku': '000001', 'quantity': 2},
                {'sku': '100000', 'quantity': 1}
            ]
        }
        self.create_order_and_assert(data)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(OrderUnit.objects.count(), 3)

    def test_invalid_order_posting(self):
        """Try to create orders with invalid parameters."""
        data_set = [
            # Missing parameter.
            {
                'name': 'Temp',
                'phone': '+375555555',
                'units': [
                    {'sku': '000000', 'quantity': 2},
                    {'sku': '000001', 'quantity': 2},
                    {'sku': '100000', 'quantity': 1}
                ]
            },
            # Invalid parameter (too long phone number).
            {
                'name': 'Temp',
                'phone': '+37555555555555555555555555555555555555555555',
                'address': '5th Str 55',
                'units': [
                    {'sku': '000000', 'quantity': 2},
                    {'sku': '000001', 'quantity': 2},
                    {'sku': '100000', 'quantity': 1}
                ]
            },
            # Invalid unit (missing sku).
            {
                'name': 'Temp',
                'phone': '+375555555',
                'address': '5th Str 55',
                'units': [
                    {'quantity': 2},
                    {'sku': '000001', 'quantity': 2},
                    {'sku': '100000', 'quantity': 1}
                ]
            },
            # Invalid unit (invalid quantity).
            {
                'name': 'Temp',
                'phone': '+375555555',
                'address': '5th Str 55',
                'units': [
                    {'sku': '000000', 'quantity': -1},
                    {'sku': '000001', 'quantity': 2},
                    {'sku': '100000', 'quantity': 1}
                ]
            },
            # Nonexistent unit.
            {
                'name': 'Temp',
                'phone': '+375555555',
                'address': '5th Str 55',
                'units': [
                    {'sku': '01010101010101001', 'quantity': 2},
                    {'sku': '000001', 'quantity': 2},
                    {'sku': '100000', 'quantity': 1}
                ]
            },
            # Unit not in stock.
            {
                'name': 'Temp',
                'phone': '+375555555',
                'address': '5th Str 55',
                'units': [
                    {'sku': '000000', 'quantity': 2},
                    {'sku': '000001', 'quantity': 2},
                    {'sku': '100002', 'quantity': 1}
                ]
            },
        ]

        for data in data_set:
            response = self.client.post(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_retrieval(self):
        """Get orders list of user."""
        self.create_order_and_assert()
        self.client.logout()

        data = self.order_data.copy()
        data['name'] = 'Temp2'

        User.objects.create_user('temp2', 'temp2@gmail.com', '123123')
        self.client.login(username='temp2', password='123123')

        self.create_order_and_assert(data)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)

    def test_order_list_when_not_logged_in(self):
        """Get orders list when not logged in (expecting 403)."""
        self.client.logout()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_retrieval(self):
        """Get single order."""
        self.create_order_and_assert()

        response = self.client.get(self.url)
        order_id = response.data[0]['id']

        url = reverse('restshop:order-detail', kwargs={'pk': order_id})
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Temp')
        self.assertEqual(len(response.data['units']), 2)

    def test_order_detail_when_unauthorized(self):
        """Get single order when user is not the owner."""
        self.create_order_and_assert()
        response = self.client.get(self.url)
        order_id = response.data[0]['id']

        self.client.logout()

        User.objects.create_user('temp2', 'temp2@gmail.com', '123123')
        self.client.login(username='temp2', password='123123')

        url = reverse('restshop:order-detail', kwargs={'pk': order_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
