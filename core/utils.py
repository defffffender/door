from django.utils.text import slugify

# Транслитерация кириллицы в латиницу для генерации URL (slug).
# slugify() сам по себе вырезает кириллицу в пустоту, поэтому сначала
# переводим буквы в латиницу.
CYRILLIC_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    # узбекские специфичные буквы
    'ў': 'o', 'қ': 'q', 'ғ': 'g', 'ҳ': 'h',
}


def translit(text):
    """Переводит кириллический текст в латиницу по таблице."""
    return ''.join(CYRILLIC_TRANSLIT.get(ch, ch) for ch in (text or '').lower())


def unique_slugify(instance, value, slug_field_name='slug'):
    """Генерирует уникальный slug из value для модели instance.

    Если такой slug уже занят другим объектом — добавляет -2, -3 и т.д.
    """
    base = slugify(translit(value)) or 'item'
    model = instance.__class__
    slug = base
    counter = 2
    qs = model.objects.all()
    if instance.pk:
        qs = qs.exclude(pk=instance.pk)
    while qs.filter(**{slug_field_name: slug}).exists():
        slug = f'{base}-{counter}'
        counter += 1
    return slug
