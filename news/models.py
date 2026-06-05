from django.db import models
from core.models import SeoMixin
from core.utils import unique_slugify


class Article(SeoMixin):
    title = models.CharField('Заголовок', max_length=300)
    slug = models.SlugField('URL', max_length=300, unique=True)
    image = models.ImageField('Изображение', upload_to='news/')
    content = models.TextField('Содержание')
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)
    is_published = models.BooleanField('Опубликовано', default=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/news/{self.slug}/'
