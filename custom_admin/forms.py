from django import forms

from core.models import (
    SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo,
)
from catalog.models import Category, Product, ProductImage
from news.models import Article
from portfolio.models import Project, ProjectImage
from contacts.models import ContactRequest


# ---------------------------------------------------------------------------
# Reusable widget helpers
# ---------------------------------------------------------------------------

TEXT_INPUT = forms.TextInput(attrs={'class': 'form-control'})
TEXT_INPUT_SLUG = forms.TextInput(attrs={'class': 'form-control slug-field'})
TEXTAREA = forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
TEXTAREA_SMALL = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
SELECT = forms.Select(attrs={'class': 'form-control'})
NUMBER_INPUT = forms.NumberInput(attrs={'class': 'form-control'})
CHECKBOX = forms.CheckboxInput(attrs={'class': 'form-check-input'})
FILE_INPUT = forms.ClearableFileInput(attrs={'class': 'form-control'})
URL_INPUT = forms.URLInput(attrs={'class': 'form-control'})
EMAIL_INPUT = forms.EmailInput(attrs={'class': 'form-control'})


def _seo_widgets():
    """Return the widget dict fragment shared by every SEO-enabled model."""
    return {
        'meta_title': forms.TextInput(attrs={'class': 'form-control'}),
        'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        'meta_keywords': forms.TextInput(attrs={'class': 'form-control'}),
    }


# ===================================================================
# Core models
# ===================================================================

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'logo', 'company_name', 'slogan', 'about_text',
            'phone', 'phone2', 'email', 'address',
            'telegram_url', 'instagram_url', 'map_embed', 'catalog_pdf',
            'telegram_bot_token', 'telegram_chat_id',
        ]
        widgets = {
            'logo': FILE_INPUT,
            'company_name': TEXT_INPUT,
            'slogan': TEXT_INPUT,
            'about_text': TEXTAREA,
            'phone': TEXT_INPUT,
            'phone2': TEXT_INPUT,
            'email': EMAIL_INPUT,
            'address': TEXT_INPUT,
            'telegram_url': URL_INPUT,
            'instagram_url': URL_INPUT,
            'map_embed': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'catalog_pdf': FILE_INPUT,
            'telegram_bot_token': TEXT_INPUT,
            'telegram_chat_id': TEXT_INPUT,
        }


class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = [
            'title', 'subtitle', 'image', 'button_text', 'button_url',
            'order', 'is_active',
        ]
        widgets = {
            'title': TEXT_INPUT,
            'subtitle': TEXTAREA_SMALL,
            'image': FILE_INPUT,
            'button_text': TEXT_INPUT,
            'button_url': URL_INPUT,
            'order': NUMBER_INPUT,
            'is_active': CHECKBOX,
        }


class AdvantageForm(forms.ModelForm):
    class Meta:
        model = Advantage
        fields = ['icon', 'title', 'description', 'order']
        widgets = {
            'icon': TEXT_INPUT,
            'title': TEXT_INPUT,
            'description': TEXTAREA_SMALL,
            'order': NUMBER_INPUT,
        }


class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = ['number', 'label', 'order']
        widgets = {
            'number': TEXT_INPUT,
            'label': TEXT_INPUT,
            'order': NUMBER_INPUT,
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'url', 'order']
        widgets = {
            'name': TEXT_INPUT,
            'logo': FILE_INPUT,
            'url': URL_INPUT,
            'order': NUMBER_INPUT,
        }


class QualityPillarForm(forms.ModelForm):
    class Meta:
        model = QualityPillar
        fields = ['title', 'description', 'image', 'order']
        widgets = {
            'title': TEXT_INPUT,
            'description': TEXTAREA,
            'image': FILE_INPUT,
            'order': NUMBER_INPUT,
        }


class PageSeoForm(forms.ModelForm):
    class Meta:
        model = PageSeo
        fields = ['page', 'meta_title', 'meta_description', 'meta_keywords']
        widgets = {
            'page': SELECT,
            **_seo_widgets(),
        }


# ===================================================================
# Catalog models
# ===================================================================

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name', 'slug', 'image', 'description', 'order',
            # SEO fields (grouped at end)
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'name': TEXT_INPUT,
            'slug': TEXT_INPUT_SLUG,
            'image': FILE_INPUT,
            'description': TEXTAREA,
            'order': NUMBER_INPUT,
            **_seo_widgets(),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'slug', 'price', 'image',
            'description', 'is_popular', 'order',
            # SEO fields (grouped at end)
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'category': SELECT,
            'name': TEXT_INPUT,
            'slug': TEXT_INPUT_SLUG,
            'price': NUMBER_INPUT,
            'image': FILE_INPUT,
            'description': TEXTAREA,
            'is_popular': CHECKBOX,
            'order': NUMBER_INPUT,
            **_seo_widgets(),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product', 'image', 'order']
        widgets = {
            'product': SELECT,
            'image': FILE_INPUT,
            'order': NUMBER_INPUT,
        }


# ===================================================================
# News models
# ===================================================================

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 'slug', 'image', 'content', 'is_published',
            # SEO fields (grouped at end)
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'title': TEXT_INPUT,
            'slug': TEXT_INPUT_SLUG,
            'image': FILE_INPUT,
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'is_published': CHECKBOX,
            **_seo_widgets(),
        }


# ===================================================================
# Portfolio models
# ===================================================================

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'image', 'description',
            # SEO fields (grouped at end)
            'meta_title', 'meta_description', 'meta_keywords',
        ]
        widgets = {
            'title': TEXT_INPUT,
            'slug': TEXT_INPUT_SLUG,
            'image': FILE_INPUT,
            'description': TEXTAREA,
            **_seo_widgets(),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['project', 'image', 'order']
        widgets = {
            'project': SELECT,
            'image': FILE_INPUT,
            'order': NUMBER_INPUT,
        }


# ===================================================================
# Contacts models
# ===================================================================

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message', 'file', 'is_read']
        widgets = {
            'name': TEXT_INPUT,
            'phone': TEXT_INPUT,
            'email': EMAIL_INPUT,
            'message': TEXTAREA,
            'file': FILE_INPUT,
            'is_read': CHECKBOX,
        }
