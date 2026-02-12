from modeltranslation.translator import register, TranslationOptions
from .models import Category, Product


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'meta_title', 'meta_description', 'meta_keywords')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'meta_title', 'meta_description', 'meta_keywords')
