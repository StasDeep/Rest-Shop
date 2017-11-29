from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rest/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('restshop.urls', namespace='restshop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [url(r'^(?P<path>.*)$', TemplateView.as_view(template_name='index.html'))]
