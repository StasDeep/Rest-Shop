from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import ProductDetailView, ProductListView, UserCreateView, SellerCreateView, OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, base_name='order')

urlpatterns = [
    url(r'^products/$', ProductListView.as_view(), name='product-list'),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product-detail'),
    url(r'^user/create/$', UserCreateView.as_view(), name='user-create'),
    url(r'^seller/create/$', SellerCreateView.as_view(), name='seller-create'),
    url(r'^', include(router.urls))
]
