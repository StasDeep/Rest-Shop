from django.conf.urls import url

from restshop.api.cart.views import CartView, CartUnitView

urlpatterns = [
    url(r'^cart/$',                          CartView.as_view(), name='cart'),
    url(r'^cart/(?P<sku>[A-Za-z\-_0-9]+)/$', CartUnitView.as_view(), name='cart-unit'),
]
