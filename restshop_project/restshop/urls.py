from django.conf.urls import url

from .views import ProductDetail, ProductList

urlpatterns = [
    url(r'^products/$', ProductList.as_view()),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetail.as_view()),
]
