from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls', namespace='shop')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('pages.urls', namespace='pages')),
    path('api-auth/', include('rest_framework.urls'))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.error_404_view'
