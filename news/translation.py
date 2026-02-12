from modeltranslation.translator import register, TranslationOptions
from .models import Article


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content', 'meta_title', 'meta_description', 'meta_keywords')
