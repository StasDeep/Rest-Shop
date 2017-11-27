from django.conf.urls import url
from rest_framework_sav.views import session_auth_view

from restshop.api.user.views import UserView, UserCreateView, SellerCreateView, ChangePasswordView, DeliveryInfoView

urlpatterns = [
    url(r'^user/$',          UserView.as_view(), name='user'),
    url(r'^user/create/$',   UserCreateView.as_view(), name='user-create'),
    url(r'^seller/create/$', SellerCreateView.as_view(), name='seller-create'),
    url(r'^deliveryinfo/$',  DeliveryInfoView.as_view(), name='delivery-info'),
    url(r'^auth/$',          session_auth_view, name='auth'),
    url(r'^password/$',      ChangePasswordView.as_view(), name='change-password'),
]
