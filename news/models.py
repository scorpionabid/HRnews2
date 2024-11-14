from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _  # Tərcümə üçün import

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
        ('draft', _('Draft')),  # Tərcümə olunan status seçimi
        ('published', _('Published')),
        ('featured', _('Featured')),
    )

    title = models.CharField(max_length=200, verbose_name=_("Başlıq"))  # Başlıq sahəsini tərcümə
    slug = models.SlugField(unique=True, blank=True, max_length=60)  # URL üçün slug
    subtitle = models.CharField(max_length=200, blank=True, verbose_name=_("Alt başlıq"))  # Tərcümə olunan alt başlıq
    content = RichTextUploadingField(verbose_name=_("Məzmun"))  # CKEditor ilə zəngin mətn sahəsi
    summary = models.TextField(blank=True, verbose_name=_("Xülasə"))  # Tərcümə olunan xülasə
    is_popular = models.BooleanField(default=False, verbose_name=_("Populyardır"))  # Tərcümə olunan sahə
    # Əlaqələr
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Kateqoriya"))  # Kateqoriya ilə əlaqə
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_("Müəllif"))  # Müəllif ilə əlaqə
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Etiketlər"))  # Tərcümə olunan etiketlər (opsional)
    
    # Media
    image = models.ImageField(upload_to='news/', blank=True, null=True, default='news/placeholder.png', verbose_name=_("Şəkil"))  # Şəkil (opsional)
    video_url = models.URLField(blank=True, null=True, verbose_name=_("Video URL"))  # Video URL (opsional)
    
    # Meta sahələr
    meta_title = models.CharField(max_length=200, blank=True, verbose_name=_("Meta başlıq"))  # Tərcümə olunan meta başlıq
    meta_description = models.TextField(blank=True, verbose_name=_("Meta təsviri"))  # Tərcümə olunan meta təsviri
    keywords = models.CharField(max_length=200, blank=True, verbose_name=_("Açar sözlər"))  # Tərcümə olunan açar sözlər
    
    # Status və göstəricilər
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name=_("Status"))  # Status
    view_count = models.PositiveIntegerField(default=0, verbose_name=_("Baxış sayı"))  # Tərcümə olunan baxış sayı
    reading_time = models.PositiveIntegerField(default=0, verbose_name=_("Oxuma müddəti (dəqiqə)"))  # Tərcümə olunan oxuma müddəti
    is_breaking = models.BooleanField(default=False, verbose_name=_("Çox önəmli xəbər"))  # Tərcümə olunan sahə
    
    # Tarixlər
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Nəşr tarixi"))  # Nəşr tarixi
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Yaradılma tarixi"))  # Yaradılma tarixi
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Yenilənmə tarixi"))  # Yenilənmə tarixi

    class Meta:
        verbose_name_plural = _("Xəbərlər")
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
