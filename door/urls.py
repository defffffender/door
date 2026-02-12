from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from core.views import switch_language

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('lang/<str:lang_code>/', switch_language, name='switch_language'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('catalog/', include('catalog.urls')),
    path('news/', include('news.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('contacts/', include('contacts.urls')),
    path('panel/', include('custom_admin.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
