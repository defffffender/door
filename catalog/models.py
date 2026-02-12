from django.db import models
from core.models import SeoMixin


class Category(SeoMixin):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/catalog/{self.slug}/'


class Product(SeoMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    price = models.DecimalField('Цена (сум)', max_digits=12, decimal_places=0, blank=True, null=True)
    image = models.ImageField('Основное изображение', upload_to='products/')
    description = models.TextField('Описание', blank=True)
    is_popular = models.BooleanField('Популярный товар', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/catalog/{self.category.slug}/{self.slug}/'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField('Изображение', upload_to='products/gallery/')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товара'
        ordering = ['order']
