from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_sav.views import session_auth_view

from .views import ProductDetailView, ProductListView, UserCreateView, SellerCreateView, OrderViewSet, TagListView, \
    PropertyListView, CartView, UserView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, base_name='order')

urlpatterns = [
    url(r'^tags/$', TagListView.as_view(), name='tag-list'),
    url(r'^properties/$', PropertyListView.as_view(), name='property-list'),
    url(r'^products/$', ProductListView.as_view(), name='product-list'),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product-detail'),
    url(r'^user/$', UserView.as_view(), name='user'),
    url(r'^user/create/$', UserCreateView.as_view(), name='user-create'),
    url(r'^seller/create/$', SellerCreateView.as_view(), name='seller-create'),
    url(r'^cart/$', CartView.as_view(), name='cart'),
    url(r'^auth/$', session_auth_view, name='auth'),
    url(r'^', include(router.urls)),
]
