from django.conf.urls import url

from restshop.api.tag.views import TagListView

urlpatterns = [
    url(r'^tags/$', TagListView.as_view(), name='tag-list'),
]
