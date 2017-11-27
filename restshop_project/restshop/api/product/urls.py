from django.conf.urls import url

from restshop.api.product.views import ProductListView, ProductDetailView

urlpatterns = [
    url(r'^products/$',                ProductListView.as_view(), name='product-list'),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view(), name='product-detail'),
]
