from django.db import models
from core.models import SeoMixin


class Project(SeoMixin):
    title = models.CharField('Название', max_length=300)
    slug = models.SlugField('URL', max_length=300, unique=True)
    image = models.ImageField('Основное изображение', upload_to='portfolio/')
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/portfolio/{self.slug}/'


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name='Проект')
    image = models.ImageField('Изображение', upload_to='portfolio/gallery/')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение проекта'
        verbose_name_plural = 'Изображения проекта'
        ordering = ['order']
