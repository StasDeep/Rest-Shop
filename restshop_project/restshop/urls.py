from django.conf.urls import url

from .views import ProductDetailView, ProductListView, UserCreateView, SellerCreateView

urlpatterns = [
    url(r'^products/$', ProductListView.as_view(), name='product_list'),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product_detail'),
    url(r'^user/create/$', UserCreateView.as_view(), name='user_create'),
    url(r'^seller/create/$', SellerCreateView.as_view(), name='seller_create'),
]
