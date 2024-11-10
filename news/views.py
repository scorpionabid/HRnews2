from django.shortcuts import render, get_object_or_404
from .models import News, Category, Ad, Partner
from django.core.paginator import Paginator

# Kateqoriya siyahısını göstərmək üçün view
def category_list(request, category_slug):
    """
    Kateqoriya üzrə xəbərləri göstərmək üçün view.
    """
    category = get_object_or_404(Category, slug=category_slug, is_active=True)  # Aktiv kateqoriyalar
    news_list = News.objects.filter(category=category, status='published').order_by('-created_at')
    paginator = Paginator(news_list, 6)  # Hər səhifədə 6 xəbər
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/category_list.html', {
        'category': category,
        'page_obj': page_obj
    })

# Xəbər detal səhifəsini göstərmək üçün view
def news_detail(request, slug):
    """
    Xəbər detalları səhifəsini göstərmək üçün view.
    """
    news = get_object_or_404(News, slug=slug, status='published')  # Yalnız yayımlanan xəbərlər göstərilir
    news.view_count += 1  # Baxış sayını artırırıq
    news.save(update_fields=['view_count'])
    return render(request, 'news/news_detail.html', {
        'news': news
    })

# Əsas səhifə üçün view
def home(request):
    """
    Əsas səhifə üçün view. Hər bir kateqoriyaya aid ən son 4 xəbəri əldə edir.
    """
    latest_news = News.objects.filter(status='published').order_by('-created_at')[:2]
    categories = Category.objects.filter(is_active=True)  # Yalnız aktiv kateqoriyalar
    ads = Ad.objects.all()
    partners = Partner.objects.all()

    # Kateqoriyalara aid ən son 4 xəbəri əldə edirik
    category_news = {}
    for category in categories:
        news_list = News.objects.filter(category=category, status='published').order_by('-created_at')[:4]
        if news_list.exists():
            category_news[category] = news_list

    return render(request, 'news/index.html', {
        'latest_news': latest_news,
        'category_news': category_news,
        'ads': ads,
        'partners': partners
    })

# Bütün xəbərləri səhifələmə ilə göstərmək üçün view
def my_view(request):
    """
    Bütün xəbərləri səhifələmə ilə göstərmək üçün view.
    """
    all_news = News.objects.filter(status='published').order_by('-created_at')  # Yalnız yayımlanan xəbərlər
    paginator = Paginator(all_news, 10)  # Hər səhifədə 10 xəbər
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/my_view.html', {
        'page_obj': page_obj
    })
