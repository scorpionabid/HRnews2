# Generated by Django 5.1.2 on 2024-11-12 12:49

import ckeditor_uploader.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_ad_description_az_ad_description_en_ad_title_az_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-published_at'], 'verbose_name_plural': 'Xəbərlər'},
        ),
        migrations.RemoveField(
            model_name='ad',
            name='description_az',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='title_az',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='title_en',
        ),
        migrations.AddField(
            model_name='news',
            name='subtitle_az',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Alt başlıq'),
        ),
        migrations.AddField(
            model_name='news',
            name='subtitle_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Alt başlıq'),
        ),
        migrations.AddField(
            model_name='news',
            name='summary_az',
            field=models.TextField(blank=True, null=True, verbose_name='Xülasə'),
        ),
        migrations.AddField(
            model_name='news',
            name='summary_en',
            field=models.TextField(blank=True, null=True, verbose_name='Xülasə'),
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.author', verbose_name='Müəllif'),
        ),
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Kateqoriya'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Məzmun'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content_az',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Məzmun'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True, verbose_name='Məzmun'),
        ),
        migrations.AlterField(
            model_name='news',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Yaradılma tarixi'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, default='news/placeholder.png', null=True, upload_to='news/', verbose_name='Şəkil'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_breaking',
            field=models.BooleanField(default=False, verbose_name='Çox önəmli xəbər'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='Populyardır'),
        ),
        migrations.AlterField(
            model_name='news',
            name='keywords',
            field=models.CharField(blank=True, max_length=200, verbose_name='Açar sözlər'),
        ),
        migrations.AlterField(
            model_name='news',
            name='meta_description',
            field=models.TextField(blank=True, verbose_name='Meta təsviri'),
        ),
        migrations.AlterField(
            model_name='news',
            name='meta_title',
            field=models.CharField(blank=True, max_length=200, verbose_name='Meta başlıq'),
        ),
        migrations.AlterField(
            model_name='news',
            name='published_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Nəşr tarixi'),
        ),
        migrations.AlterField(
            model_name='news',
            name='reading_time',
            field=models.PositiveIntegerField(default=0, verbose_name='Oxuma müddəti (dəqiqə)'),
        ),
        migrations.AlterField(
            model_name='news',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('featured', 'Featured')], default='draft', max_length=10, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='news',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200, verbose_name='Alt başlıq'),
        ),
        migrations.AlterField(
            model_name='news',
            name='summary',
            field=models.TextField(blank=True, verbose_name='Xülasə'),
        ),
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(blank=True, to='news.tag', verbose_name='Etiketlər'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Başlıq'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title_az',
            field=models.CharField(max_length=200, null=True, verbose_name='Başlıq'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Başlıq'),
        ),
        migrations.AlterField(
            model_name='news',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Yenilənmə tarixi'),
        ),
        migrations.AlterField(
            model_name='news',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='Video URL'),
        ),
        migrations.AlterField(
            model_name='news',
            name='view_count',
            field=models.PositiveIntegerField(default=0, verbose_name='Baxış sayı'),
        ),
    ]