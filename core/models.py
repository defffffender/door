from django.db import models


class SeoMixin(models.Model):
    meta_title = models.CharField('SEO Title', max_length=300, blank=True)
    meta_description = models.TextField('SEO Description', blank=True)
    meta_keywords = models.CharField('SEO Keywords', max_length=500, blank=True)

    class Meta:
        abstract = True


class PageSeo(SeoMixin):
    PAGE_CHOICES = [
        ('home', 'Главная'),
        ('about', 'О компании'),
        ('catalog', 'Каталог'),
        ('news', 'Новости'),
        ('portfolio', 'Наши работы'),
        ('contacts', 'Контакты'),
    ]
    page = models.CharField('Страница', max_length=50, choices=PAGE_CHOICES, unique=True)

    class Meta:
        verbose_name = 'SEO страницы'
        verbose_name_plural = 'SEO страниц'

    def __str__(self):
        return self.get_page_display()


class SiteSettings(models.Model):
    logo = models.ImageField('Логотип', upload_to='settings/', blank=True)
    company_name = models.CharField('Название компании', max_length=200, default='Door Company')
    slogan = models.CharField('Слоган', max_length=300, blank=True)
    about_text = models.TextField('О компании (краткое)', blank=True)
    phone = models.CharField('Телефон', max_length=50, blank=True)
    phone2 = models.CharField('Телефон 2', max_length=50, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адрес', max_length=300, blank=True)
    telegram_url = models.URLField('Telegram', blank=True)
    instagram_url = models.URLField('Instagram', blank=True)
    map_embed = models.TextField('Код карты (iframe)', blank=True)
    catalog_pdf = models.FileField('PDF-каталог', upload_to='catalog/', blank=True, help_text='PDF-файл каталога для скачивания')
    telegram_bot_token = models.CharField('Telegram Bot Token', max_length=200, blank=True, help_text='Токен бота от @BotFather')
    telegram_chat_id = models.CharField('Telegram Chat ID', max_length=100, blank=True, help_text='ID чата/группы для уведомлений')

    # Theme
    theme_primary = models.CharField('Основной цвет', max_length=20, default='#1b4f8a', help_text='Кнопки, ссылки, акценты')
    theme_primary_hover = models.CharField('Основной (ховер)', max_length=20, default='#153f6e')
    theme_dark = models.CharField('Тёмный цвет', max_length=20, default='#1a2d45', help_text='Хедер, тёмные секции')
    theme_accent = models.CharField('Светлый акцент', max_length=20, default='#8ab4e8', help_text='Иконки, подсветки')
    theme_bg_light = models.CharField('Светлый фон', max_length=20, default='#f5f7fa', help_text='Фон секций')
    theme_bg_accent = models.CharField('Акцентный фон', max_length=20, default='#f8fafe')
    theme_text = models.CharField('Цвет текста', max_length=20, default='#333333')
    theme_text_light = models.CharField('Вторичный текст', max_length=20, default='#777777')
    theme_success = models.CharField('Цвет успеха', max_length=20, default='#1b8a4b')
    theme_danger = models.CharField('Цвет ошибки', max_length=20, default='#e8433e')
    theme_warning = models.CharField('Цвет предупреждения', max_length=20, default='#f5a623', help_text='Бейджи "Популярное"')
    theme_font = models.CharField('Шрифт', max_length=100, default='Inter', help_text='Название Google Fonts шрифта')

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Banner(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Подзаголовок', max_length=300, blank=True)
    image = models.ImageField('Изображение', upload_to='banners/')
    button_text = models.CharField('Текст кнопки', max_length=100, default='Связаться с нами')
    button_url = models.CharField('Ссылка кнопки', max_length=300, default='/contacts/')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ['order']

    def __str__(self):
        return self.title


class Advantage(models.Model):
    icon = models.CharField('CSS-класс иконки', max_length=100, blank=True)
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'
        ordering = ['order']

    def __str__(self):
        return self.title


class Statistic(models.Model):
    number = models.CharField('Число', max_length=50)
    label = models.CharField('Подпись', max_length=200)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'
        ordering = ['order']

    def __str__(self):
        return f'{self.number} — {self.label}'


class Partner(models.Model):
    name = models.CharField('Название', max_length=200)
    logo = models.ImageField('Логотип', upload_to='partners/')
    url = models.URLField('Ссылка', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
        ordering = ['order']

    def __str__(self):
        return self.name


class QualityPillar(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='quality/', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Столп качества'
        verbose_name_plural = 'Столпы качества'
        ordering = ['order']

    def __str__(self):
        return self.title
