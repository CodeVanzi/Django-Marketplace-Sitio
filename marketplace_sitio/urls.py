from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path




urlpatterns = [
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('mestre/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('a_users.urls')),
    path('commodities/', include('commodities.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)