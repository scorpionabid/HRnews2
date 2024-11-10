from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Xəbər limiti - yalnız ən son 100 xəbər saxlanılsın
NEWS_LIMIT = 100  # Maksimum saxlanacaq xəbər sayı

# Kateqoriya modeli
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Kateqoriya adı (unikal)
    slug = models.SlugField(unique=True, blank=True)  # URL üçün slug
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories'
    )  # Alt kateqoriyalar üçün əlaqə
    description = models.TextField(blank=True)  # Kateqoriyanın təsviri (opsional)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # Kateqoriya şəkli (opsional)
    meta_title = models.CharField(max_length=200, blank=True)  # Meta başlıq
    meta_description = models.TextField(blank=True)  # Meta təsviri
    order = models.IntegerField(default=0)  # Sıra
    is_active = models.BooleanField(default=True)  # Aktivlik statusu
    created_at = models.DateTimeField(auto_now_add=True)  # Yaradılma tarixi
    updated_at = models.DateTimeField(auto_now=True)  # Yenilənmə tarixi

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']  # Sıra və ad əsasında sıralama

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Slug avtomatik olaraq ad əsasında yaradılır (əgər mövcud deyilsə)."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

# Tag modeli (xəbərlərə aid etiketi təmsil edir)
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Tag adı
    slug = models.SlugField(unique=True, blank=True)  # URL üçün slug
    description = models.TextField(blank=True)  # Etiket təsviri (opsional)

    def save(self, *args, **kwargs):
        """Slug avtomatik olaraq ad əsasında yaradılır (əgər mövcud deyilsə)."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Müəllif modeli
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Müəllif ilə istifadəçi əlaqəsi
    bio = models.TextField()  # Bioqrafiya
    profile_picture = models.ImageField(upload_to='authors/', blank=True, null=True)  # Profil şəkli
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

# Xəbər modeli
class News(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('featured', 'Featured'),
    )

    title = models.CharField(max_length=200)  # Başlıq
    slug = models.SlugField(unique=True, blank=True)  # URL üçün slug
    subtitle = models.CharField(max_length=200, blank=True)  # Alt başlıq
    content = RichTextUploadingField()  # CKEditor ilə zəngin mətn sahəsi
    summary = models.TextField(blank=True)  # Xülasə
    is_popular = models.BooleanField(default=False)
    # Əlaqələr
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Kateqoriya ilə əlaqə
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Müəllif ilə əlaqə
    tags = models.ManyToManyField(Tag, blank=True)  # Etiketlər (opsional)
    
    # Media
    image = models.ImageField(upload_to='news/', blank=True, null=True)  # Şəkil (opsional)
    video_url = models.URLField(blank=True, null=True)  # Video URL (opsional)
    
    # Meta sahələr
    meta_title = models.CharField(max_length=200, blank=True)  # Meta başlıq
    meta_description = models.TextField(blank=True)  # Meta təsviri
    keywords = models.CharField(max_length=200, blank=True)  # Açar sözlər (opsional)
    
    # Status və göstəricilər
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')  # Status
    view_count = models.PositiveIntegerField(default=0)  # Baxış sayı
    reading_time = models.PositiveIntegerField(default=0)  # Oxuma müddəti (dəqiqə)
    is_breaking = models.BooleanField(default=False)  # Çox önəmli xəbər
    
    # Tarixlər
    published_at = models.DateTimeField(null=True, blank=True)  # Nəşr tarixi
    created_at = models.DateTimeField(auto_now_add=True)  # Yaradılma tarixi
    updated_at = models.DateTimeField(auto_now=True)  # Yenilənmə tarixi

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-published_at']  # Ən son nəşr tarixinə görə sıralama

    def save(self, *args, **kwargs):
        """Slug avtomatik olaraq başlıq əsasında yaradılır (əgər mövcud deyilsə)."""
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.reading_time:
            word_count = len(self.content.split())
            self.reading_time = round(word_count / 200)  # Təxminən 200 söz/dəqiqə
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# Reklam modeli
class Advertisement(models.Model):
    POSITION_CHOICES = (
        ('header', 'Header'),
        ('sidebar', 'Sidebar'),
        ('content', 'Content'),
        ('footer', 'Footer'),
    )

    name = models.CharField(max_length=100)  # Reklam adı
    client = models.CharField(max_length=100)  # Müştəri adı
    image = models.ImageField(upload_to='ads/')  # Reklam şəkli
    url = models.URLField()  # URL
    position = models.CharField(max_length=20, choices=POSITION_CHOICES)  # Mövqe
    start_date = models.DateTimeField()  # Başlama tarixi
    end_date = models.DateTimeField()  # Bitmə tarixi
    is_active = models.BooleanField(default=True)  # Aktivlik statusu
    impressions = models.PositiveIntegerField(default=0)  # Baxış sayı
    clicks = models.PositiveIntegerField(default=0)  # Klik sayı
    created_at = models.DateTimeField(auto_now_add=True)  # Yaradılma tarixi

    def __str__(self):
        return self.name

# Partnyor modeli
class Partner(models.Model):
    name = models.CharField(max_length=100)  # Partnyor adı
    logo = models.ImageField(upload_to='partners_logos/')  # Logo
    website_url = models.URLField(blank=True, null=True)  # Vebsayt URL (opsional)

    def __str__(self):
        return self.name

# Yuxarıdakı modellərə əlavə olaraq digər modellər və konfiqurasiyalar üçün də eyni şəkildə təkmilləşdirmələr edilə bilər.
# Reklam modeli
class Ad(models.Model):
    title = models.CharField(max_length=255)  # Reklam başlığı
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)  # Reklam şəkli
    description = models.TextField(blank=True, null=True)  # Reklamın təsviri
    link = models.URLField(blank=True, null=True)  # Reklama aid URL linki
    created_at = models.DateTimeField(auto_now_add=True)  # Yaradılma tarixi
    is_active = models.BooleanField(default=True)  # Aktivlik statusu

    class Meta:
        ordering = ['-created_at']  # Ən yeni reklamlar əvvəl görünəcək
        verbose_name_plural = "Ads"  # Admin panelində çoxluq forması

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Şəkil optimallaşdırılması zamanı şəkilin ölçüsünü dəyişmək.
        """
        super().save(*args, **kwargs)
        if self.image:
            from PIL import Image
            import os
            image_path = self.image.path
            try:
                with Image.open(image_path) as img:
                    img = img.resize((600, 400), Image.Resampling.LANCZOS)
                    img.save(image_path)
            except Exception as e:
                print(f"Şəkil optimallaşdırılması zamanı səhv baş verdi: {e}")
