from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib import admin

#favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage_new.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^online/", include("online.urls")),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/site_media/static/favicon/favicon.ico', permanent=True))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
