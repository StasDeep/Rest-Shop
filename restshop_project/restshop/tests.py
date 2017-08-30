from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Order, Product, Seller, Unit, OrderUnit


class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('restshop:order_create')
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
        Unit.objects.create(product=product, sku='100002', price=95, in_stock=False)

    def test_create_order(self):
        """Create a new order object."""
        data = {
            'name': 'Temp',
            'phone': '+375555555',
            'address': '5th Str 55',
            'units': [
                {'sku': '000000', 'quantity': 2},
                {'sku': '000001', 'quantity': 2}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderUnit.objects.count(), 2)

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
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
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
