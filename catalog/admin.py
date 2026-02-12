from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'category', 'price', 'is_popular', 'order')
    list_editable = ('is_popular', 'order')
    list_filter = ('category', 'is_popular')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
