from modeltranslation.translator import register, TranslationOptions
from .models import SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('company_name', 'slogan', 'about_text', 'address')


@register(Banner)
class BannerTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'button_text')


@register(Advantage)
class AdvantageTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Statistic)
class StatisticTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(QualityPillar)
class QualityPillarTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(PageSeo)
class PageSeoTranslationOptions(TranslationOptions):
    fields = ('meta_title', 'meta_description', 'meta_keywords')
