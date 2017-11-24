from django.conf.urls import url

from restshop.api.property.views import PropertyListView

urlpatterns = [
    url(r'^properties/$', PropertyListView.as_view(), name='property-list'),
]
