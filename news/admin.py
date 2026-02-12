from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Article


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('title', 'created_at', 'is_published')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
