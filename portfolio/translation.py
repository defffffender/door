from modeltranslation.translator import register, TranslationOptions
from .models import Project


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'meta_title', 'meta_description', 'meta_keywords')
