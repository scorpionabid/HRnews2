"""
URL configuration for hrnews project.

The `urlpatterns` list routes URLs to views. For more information, please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.urls import path, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.conf.urls.static import static

# Əsas URL nümunələri
urlpatterns = [
    path('admin/', admin.site.urls),
    # Dil prefiksi ilə işləməyən digər əsas URL-lər burada yerləşdirilə bilər
    path('ckeditor/', include('ckeditor_uploader.urls')),  # CKEditor üçün yol
]

# Dil prefiksini əlavə edən URL nümunələri
urlpatterns += i18n_patterns(
    path('', include('news.urls')),  # `news` tətbiqinin URL-ləri
    prefix_default_language=False  # Əsas dil prefiksi göstərilməyəcək
)

# Yalnız DEBUG rejimində media faylları göstərilir
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
