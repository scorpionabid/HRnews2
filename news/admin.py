from django.contrib import admin
from .models import Category, News, Ad, Partner, Tag, Author, Advertisement
from django.utils.html import format_html
from django.db.models import Count
from ckeditor.widgets import CKEditorWidget
from django import forms
from PIL import Image

# CKEditor ilə xəbər forması
class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # CKEditor ilə zəngin mətn sahəsi

    class Meta:
        model = News
        fields = '__all__'

# Kateqoriyalar üçün default məlumatların yaradılması funksiyası
def create_default_categories():
    """Default kateqoriyalar yaradılır."""
    default_categories = [
        "Əsas Xəbərlər", "Görüşlər", "Təlimlər", 
        "Vakansiyalar", "Dünya", "Texnologiya", "Biznes"
    ]
    for category_name in default_categories:
        Category.objects.get_or_create(name=category_name)

# Kateqoriya modelinin admin interfeysi
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Kateqoriyaların idarə olunması üçün admin paneli."""
    list_display = ['name', 'parent', 'created_at', 'is_active']
    search_fields = ['name']
    list_filter = ['parent', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    def save_model(self, request, obj, form, change):
        """Modelin saxlanılması zamanı default kateqoriyalar yaradılır."""
        super().save_model(request, obj, form, change)
        create_default_categories()

# Xəbər modelinin admin interfeysi
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    """Xəbərlərin idarə olunması üçün admin paneli."""
    form = NewsForm
    list_display = ['title', 'category', 'created_at', 'author', 'is_popular', 'view_count']
    search_fields = ['title', 'content']
    list_filter = ['category', 'created_at', 'status', 'is_breaking']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    actions = ['approve_news']
    readonly_fields = ['preview_image']
    list_editable = ['is_popular']

    def preview_image(self, obj):
        """Xəbərlərin şəkil önizləməsi."""
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "Şəkil yoxdur"
    preview_image.short_description = "Şəkil Önizləmə"

    def save_model(self, request, obj, form, change):
        """Modelin saxlanılması zamanı şəkil optimallaşdırması."""
        super().save_model(request, obj, form, change)
        if obj.image:
            image_path = obj.image.path
            try:
                with Image.open(image_path) as img:
                    img = img.resize((600, 400), Image.Resampling.LANCZOS)
                    img.save(image_path)
            except Exception as e:
                self.message_user(request, f"Şəkil optimallaşdırılması zamanı səhv baş verdi: {e}", level="error")

    def approve_news(self, request, queryset):
        """Xüsusi fəaliyyət: Xəbərləri populyar statusa gətir."""
        queryset.update(is_popular=True)
        self.message_user(request, "Seçilmiş xəbərlər populyar statusa gətirildi.")
    approve_news.short_description = "Seçilmiş xəbərləri populyar et"

# Reklam modelinin admin interfeysi
@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Reklamların idarə olunması üçün admin paneli."""
    list_display = ['title', 'created_at']
    search_fields = ['title']
    list_filter = ['created_at']

    def save_model(self, request, obj, form, change):
        """Modelin saxlanılması zamanı şəkil optimallaşdırması."""
        super().save_model(request, obj, form, change)
        if obj.image:
            image_path = obj.image.path
            try:
                with Image.open(image_path) as img:
                    img = img.resize((500, 500), Image.Resampling.LANCZOS)
                    img.save(image_path)
            except Exception as e:
                self.message_user(request, f"Şəkil optimallaşdırılması zamanı səhv baş verdi: {e}", level="error")

# Partnyor modelinin admin interfeysi
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url')

# Default kateqoriyaların yaradılması üçün xüsusi fəaliyyət
admin.site.add_action(create_default_categories, "create_default_categories")

# Digər modellər (Tag, Author, Advertisement və s.) əlavə oluna bilər.
