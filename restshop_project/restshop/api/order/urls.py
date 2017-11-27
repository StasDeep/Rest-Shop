from django.conf.urls import url

from restshop.api.order.views import OrderView, OrderDetailView

urlpatterns = [
    url(r'^orders/$',                OrderView.as_view(), name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$', OrderDetailView.as_view(), name='order-detail'),
]
