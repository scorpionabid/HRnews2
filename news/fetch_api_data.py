import requests
from .models import News, Category, Author
from django.utils.text import slugify
from datetime import datetime
from django.utils import timezone  # Zaman zonası dəstəyi üçün
from django.conf import settings
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
import os
import pytz

# API açarı və URL
API_KEY = settings.NEWS_API_KEY
URL = 'https://newsapi.org/v2/everything'

# Placeholder şəkil yolu
PLACEHOLDER_IMAGE_PATH = 'media/news/placeholder.png'  # Placeholder şəkil yolu

def fetch_and_store_news(query, category_slug, category_name):
    """
    Xəbərləri News API-dən çəkir və müəyyən kateqoriyada saxlayır.
    :param query: APİ sorğusu üçün axtarış sorğusu.
    :param category_slug: Kateqoriya slug-i.
    :param category_name: Kateqoriya adı.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    params = {
        'q': query,
        'language': 'en',
        'sortBy': 'popularity',  # Reytingi yüksək olan xəbərlər
        'apiKey': API_KEY,
        'pageSize': 5  # Maksimum 5 xəbər çəkmək
    }
    response = requests.get(URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])

        # Kateqoriyanı yaradın və ya tapın
        category, _ = Category.objects.get_or_create(name=category_name, slug=category_slug)

        for article in articles:
            slug = slugify(article['title'])

            # Şəkil yoxlanması və saxlanması
            image_url = article.get('urlToImage')
            image = None
            if image_url:
                try:
                    img_response = requests.get(image_url, headers=headers, stream=True)
                    if img_response.status_code == 200:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(img_response.content)
                        img_temp.flush()
                        image = File(img_temp, name=f"{slug}.jpg")
                    else:
                        print(f"Şəkil yükləmə zamanı HTTP səhvi: {img_response.status_code}")
                except Exception as e:
                    print(f"Şəkil yükləmə zamanı xəta: {e}")
            else:
                # Placeholder şəkil təyin etmək
                if os.path.exists(PLACEHOLDER_IMAGE_PATH):
                    with open(PLACEHOLDER_IMAGE_PATH, 'rb') as placeholder_file:
                        image = File(placeholder_file, name='placeholder.png')
                else:
                    print(f"Placeholder şəkil tapılmadı: {PLACEHOLDER_IMAGE_PATH}")

            # Zaman zonası məlumatını tətbiq edin
            try:
                published_at = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                published_at = published_at.replace(tzinfo=pytz.UTC)  # Zaman zonası əlavə edilir
            except Exception as e:
                print(f"Tarix formatlama zamanı xəta: {e}")
                published_at = timezone.now()  # Fallback olaraq indiki zaman istifadə edilir

            # Xəbəri yaradın və ya mövcud olub olmadığını yoxlayın
            news, created = News.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': article['title'],
                    'content': f"{article.get('description') or article.get('content') or ''} <br> Daha çox oxumaq üçün <a href='{article.get('url')}' target='_blank'>buraya klikləyin</a>",
                    'category': category,
                    'author': Author.objects.first(),  # İlk mövcud müəllif
                    'published_at': published_at,
                    'status': 'published'
                }
            )

            # Yeni yaradılan xəbər üçün şəkil əlavə edin
            if created and image:
                news.image.save(image.name, image)
                news.save()

            # Xəbər limiti yoxlaması - maksimum 10 xəbər
            news_count = News.objects.filter(category=category).count()
            if news_count > 10:
                oldest_news = News.objects.filter(category=category).order_by('published_at').first()
                if oldest_news:
                    oldest_news.delete()

    else:
        print(f"APİ sorğusu zamanı səhv baş verdi: {response.status_code}")
