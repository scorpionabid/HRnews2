from .models import Category, Ad

def categories(request):
    """Aktiv kateqoriyaları gətirir."""
    categories = Category.objects.filter(is_active=True).order_by('name')  # Kateqoriyalar sıralanır və yalnız aktiv olanlar alınır
    return {'categories': categories}

def ads_processor(request):
    """Ən son iki reklamı alır."""
    ads = Ad.objects.filter(is_active=True).order_by('-created_at')[:2]  # Yalnız aktiv reklamları ən yenilərdən başlayaraq alırıq
    return {'ads': ads}
