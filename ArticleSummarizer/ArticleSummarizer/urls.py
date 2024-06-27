from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from summarizer import views as summarizer_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('summarizer.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = summarizer_views.custom_404
handler500 = summarizer_views.custom_500
