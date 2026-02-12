from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(TranslationAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Advantage)
class AdvantageAdmin(TranslationAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(Statistic)
class StatisticAdmin(TranslationAdmin):
    list_display = ('number', 'label', 'order')
    list_editable = ('order',)


@admin.register(Partner)
class PartnerAdmin(TranslationAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(QualityPillar)
class QualityPillarAdmin(TranslationAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


@admin.register(PageSeo)
class PageSeoAdmin(TranslationAdmin):
    list_display = ('page', 'meta_title')
