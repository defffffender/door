from django import forms

from modeltranslation.translator import translator
from modeltranslation.utils import build_localized_fieldname

from core.models import (
    SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo,
)
from catalog.models import Category, Product, ProductImage
from news.models import Article
from portfolio.models import Project, ProjectImage
from contacts.models import ContactRequest


# ---------------------------------------------------------------------------
# Multi-language helpers (django-modeltranslation)
# ---------------------------------------------------------------------------

LANGUAGES = ['ru', 'uz', 'en']
DEFAULT_LANG = 'ru'
LANG_LABELS = {'ru': 'RU', 'uz': 'UZ', 'en': 'EN'}


# ---------------------------------------------------------------------------
# Reusable widget factories
#
# Factories (not shared instances) are used so every form field — including the
# per-language variants generated below — gets its own widget object.
# ---------------------------------------------------------------------------

def text_input():
    return forms.TextInput(attrs={'class': 'form-control'})


def slug_input():
    return forms.TextInput(attrs={'class': 'form-control slug-field'})


def textarea():
    return forms.Textarea(attrs={'class': 'form-control', 'rows': 4})


def textarea_small():
    return forms.Textarea(attrs={'class': 'form-control', 'rows': 3})


def textarea_large():
    return forms.Textarea(attrs={'class': 'form-control', 'rows': 10})


def select():
    return forms.Select(attrs={'class': 'form-control'})


def number_input():
    return forms.NumberInput(attrs={'class': 'form-control'})


def checkbox():
    return forms.CheckboxInput(attrs={'class': 'form-check-input'})


def file_input():
    return forms.ClearableFileInput(attrs={'class': 'form-control'})


def url_input():
    return forms.URLInput(attrs={'class': 'form-control'})


def email_input():
    return forms.EmailInput(attrs={'class': 'form-control'})


def color_input():
    return forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': 'color'})


def map_textarea():
    return forms.Textarea(attrs={'class': 'form-control', 'rows': 5})


def build_meta(model, specs):
    """Build (fields, widgets) for a ModelForm Meta from ordered specs.

    ``specs`` is a list of ``(field_name, widget_factory)`` tuples. Any field
    that is translatable (registered with modeltranslation) is expanded into
    its per-language variants — e.g. ``name`` becomes ``name_ru``, ``name_uz``,
    ``name_en`` — so all three languages can be edited side by side in /panel/.
    """
    try:
        translatable = set(translator.get_options_for_model(model).fields)
    except Exception:
        translatable = set()

    fields = []
    widgets = {}
    for name, factory in specs:
        if name in translatable:
            for lang in LANGUAGES:
                loc = build_localized_fieldname(name, lang)
                fields.append(loc)
                widgets[loc] = factory()
        else:
            fields.append(name)
            widgets[name] = factory()
    return fields, widgets


class TranslatedModelForm(forms.ModelForm):
    """Adds language suffix labels (RU/UZ/EN) to translated fields.

    The Russian (default-language) variant keeps the original required state;
    the Uzbek and English variants are always optional, so partial translations
    are allowed — empty ones fall back to Russian on the site.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model = self._meta.model
        try:
            bases = translator.get_options_for_model(model).fields
        except Exception:
            bases = ()
        for base in bases:
            try:
                model_field = model._meta.get_field(base)
                base_label = model_field.verbose_name
                base_required = not model_field.blank
            except Exception:
                base_label, base_required = base, False
            for lang in LANGUAGES:
                loc = build_localized_fieldname(base, lang)
                if loc in self.fields:
                    self.fields[loc].label = f'{base_label} ({LANG_LABELS[lang]})'
                    self.fields[loc].required = (
                        base_required if lang == DEFAULT_LANG else False
                    )


class SlugOptionalMixin:
    """Делает поле URL (slug) необязательным.

    Если оставить пустым — slug сгенерируется автоматически из названия
    (см. save() в моделях).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'slug' in self.fields:
            self.fields['slug'].required = False
            self.fields['slug'].widget.attrs['placeholder'] = (
                'Оставьте пустым — создастся автоматически'
            )


# ===================================================================
# Core models
# ===================================================================

class SiteSettingsForm(TranslatedModelForm):
    class Meta:
        model = SiteSettings
        fields, widgets = build_meta(SiteSettings, [
            ('logo', file_input),
            ('favicon', file_input),
            ('company_name', text_input),
            ('slogan', text_input),
            ('about_text', textarea),
            ('about_image', file_input),
            ('phone', text_input),
            ('phone2', text_input),
            ('email', email_input),
            ('address', text_input),
            ('telegram_url', url_input),
            ('instagram_url', url_input),
            ('map_embed', map_textarea),
            ('catalog_pdf', file_input),
            ('telegram_bot_token', text_input),
            ('telegram_chat_id', text_input),
            # Theme
            ('theme_primary', color_input),
            ('theme_primary_hover', color_input),
            ('theme_dark', color_input),
            ('theme_accent', color_input),
            ('theme_bg_light', color_input),
            ('theme_bg_accent', color_input),
            ('theme_text', color_input),
            ('theme_text_light', color_input),
            ('theme_success', color_input),
            ('theme_danger', color_input),
            ('theme_warning', color_input),
            ('theme_font', text_input),
        ])


class BannerForm(TranslatedModelForm):
    class Meta:
        model = Banner
        fields, widgets = build_meta(Banner, [
            ('title', text_input),
            ('subtitle', textarea_small),
            ('image', file_input),
            ('button_text', text_input),
            ('button_url', url_input),
            ('order', number_input),
            ('is_active', checkbox),
        ])


class AdvantageForm(TranslatedModelForm):
    class Meta:
        model = Advantage
        fields, widgets = build_meta(Advantage, [
            ('icon', text_input),
            ('title', text_input),
            ('description', textarea_small),
            ('order', number_input),
        ])


class StatisticForm(TranslatedModelForm):
    class Meta:
        model = Statistic
        fields, widgets = build_meta(Statistic, [
            ('number', text_input),
            ('label', text_input),
            ('order', number_input),
        ])


class PartnerForm(TranslatedModelForm):
    class Meta:
        model = Partner
        fields, widgets = build_meta(Partner, [
            ('name', text_input),
            ('logo', file_input),
            ('url', url_input),
            ('order', number_input),
        ])


class QualityPillarForm(TranslatedModelForm):
    class Meta:
        model = QualityPillar
        fields, widgets = build_meta(QualityPillar, [
            ('title', text_input),
            ('description', textarea),
            ('image', file_input),
            ('order', number_input),
        ])


class PageSeoForm(TranslatedModelForm):
    class Meta:
        model = PageSeo
        fields, widgets = build_meta(PageSeo, [
            ('page', select),
            ('meta_title', text_input),
            ('meta_description', textarea_small),
            ('meta_keywords', text_input),
        ])


# ===================================================================
# Catalog models
# ===================================================================

class CategoryForm(SlugOptionalMixin, TranslatedModelForm):
    class Meta:
        model = Category
        fields, widgets = build_meta(Category, [
            ('name', text_input),
            ('slug', slug_input),
            ('image', file_input),
            ('description', textarea),
            ('order', number_input),
            # SEO fields (grouped at end)
            ('meta_title', text_input),
            ('meta_description', textarea_small),
            ('meta_keywords', text_input),
        ])


class ProductForm(SlugOptionalMixin, TranslatedModelForm):
    class Meta:
        model = Product
        fields, widgets = build_meta(Product, [
            ('category', select),
            ('name', text_input),
            ('slug', slug_input),
            ('price', number_input),
            ('image', file_input),
            ('description', textarea),
            ('is_popular', checkbox),
            ('order', number_input),
            # SEO fields (grouped at end)
            ('meta_title', text_input),
            ('meta_description', textarea_small),
            ('meta_keywords', text_input),
        ])


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'order']
        widgets = {
            'product': select(),
            'image': file_input(),
            'order': number_input(),
        }


# ===================================================================
# News models
# ===================================================================

class ArticleForm(SlugOptionalMixin, TranslatedModelForm):
    class Meta:
        model = Article
        fields, widgets = build_meta(Article, [
            ('title', text_input),
            ('slug', slug_input),
            ('image', file_input),
            ('content', textarea_large),
            ('is_published', checkbox),
            # SEO fields (grouped at end)
            ('meta_title', text_input),
            ('meta_description', textarea_small),
            ('meta_keywords', text_input),
        ])


# ===================================================================
# Portfolio models
# ===================================================================

class ProjectForm(SlugOptionalMixin, TranslatedModelForm):
    class Meta:
        model = Project
        fields, widgets = build_meta(Project, [
            ('title', text_input),
            ('slug', slug_input),
            ('image', file_input),
            ('description', textarea),
            # SEO fields (grouped at end)
            ('meta_title', text_input),
            ('meta_description', textarea_small),
            ('meta_keywords', text_input),
        ])


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['project', 'image', 'order']
        widgets = {
            'project': select(),
            'image': file_input(),
            'order': number_input(),
        }


# ===================================================================
# Contacts models
# ===================================================================

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message', 'file', 'is_read']
        widgets = {
            'name': text_input(),
            'phone': text_input(),
            'email': email_input(),
            'message': textarea(),
            'file': file_input(),
            'is_read': checkbox(),
        }
