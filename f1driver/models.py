from django.db import models
from django.urls import reverse


class Driver(models.Model):
    title = models.CharField(max_length=250, verbose_name='Имя пилота')
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(verbose_name='О пилоте', blank=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото пилота')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Метка публикации')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория', related_name='get_posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('driver:post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Известный гонщик'
        verbose_name_plural = 'Известные гонщики'
        ordering = ['-time_create', 'title']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('driver:category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['name']
# Create your models here.
