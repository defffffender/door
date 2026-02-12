from django.db import models


class ContactRequest(models.Model):
    name = models.CharField('Имя', max_length=200)
    phone = models.CharField('Телефон', max_length=50)
    email = models.EmailField('Email', blank=True)
    message = models.TextField('Сообщение', blank=True)
    file = models.FileField('Файл', upload_to='contact_files/', blank=True)
    created_at = models.DateTimeField('Дата отправки', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.phone} ({self.created_at:%d.%m.%Y})'
