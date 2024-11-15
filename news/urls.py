from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Tətbiq daxilindəki URL nümunələri
urlpatterns = [
    path('', views.home, name='home'),  # Əsas səhifə üçün URL
    path('search/', views.search_view, name='search'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),  # Xəbər detalları üçün URL
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),  # Kateqoriya üzrə xəbərlər üçün URL
]

# Yalnız DEBUG rejimində media faylları göstərilir
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
