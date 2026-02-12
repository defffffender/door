from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import SiteSettings, Banner, Advantage, Statistic, Partner, QualityPillar, PageSeo
from catalog.models import Category, Product, ProductImage
from news.models import Article
from portfolio.models import Project, ProjectImage
from contacts.models import ContactRequest

from .forms import (
    SiteSettingsForm, BannerForm, AdvantageForm, StatisticForm,
    PartnerForm, QualityPillarForm, PageSeoForm, CategoryForm,
    ProductForm, ArticleForm, ProjectForm,
)

LOGIN_URL = '/panel/login/'


# =============================================================================
# Auth
# =============================================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('panel_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/panel/')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'custom_admin/login.html')


@login_required(login_url=LOGIN_URL)
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('panel_login')


# =============================================================================
# Dashboard
# =============================================================================

@login_required(login_url=LOGIN_URL)
def dashboard(request):
    context = {
        'product_count': Product.objects.count(),
        'category_count': Category.objects.count(),
        'article_count': Article.objects.count(),
        'project_count': Project.objects.count(),
        'unread_contacts_count': ContactRequest.objects.filter(is_read=False).count(),
    }
    return render(request, 'custom_admin/dashboard.html', context)


# =============================================================================
# SiteSettings (singleton)
# =============================================================================

@login_required(login_url=LOGIN_URL)
def settings_edit(request):
    obj = SiteSettings.load()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Настройки сайта обновлены.')
            return redirect('panel_settings')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = SiteSettingsForm(instance=obj)
    return render(request, 'custom_admin/settings_form.html', {'form': form})


# =============================================================================
# Generic CRUD helpers
# =============================================================================

def _list_view(request, model, template, context_name):
    objects = model.objects.all()
    return render(request, template, {context_name: objects})


def _create_view(request, form_class, template, redirect_url, extra_save=None):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            if extra_save:
                extra_save(request, obj)
            messages.success(request, 'Запись успешно создана.')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = form_class()
    return render(request, template, {'form': form})


def _edit_view(request, model, pk, form_class, template, redirect_url, extra_save=None):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            if extra_save:
                extra_save(request, obj)
            messages.success(request, 'Запись успешно обновлена.')
            return redirect(redirect_url)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = form_class(instance=obj)
    return render(request, template, {'form': form, 'object': obj})


def _delete_view(request, model, pk, template, redirect_url):
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Запись успешно удалена.')
        return redirect(redirect_url)
    return render(request, template, {'object': obj})


# =============================================================================
# Banner
# =============================================================================

@login_required(login_url=LOGIN_URL)
def banner_list(request):
    return _list_view(request, Banner, 'custom_admin/banner_list.html', 'banners')


@login_required(login_url=LOGIN_URL)
def banner_create(request):
    return _create_view(request, BannerForm, 'custom_admin/banner_form.html', 'panel_banner_list')


@login_required(login_url=LOGIN_URL)
def banner_edit(request, pk):
    return _edit_view(request, Banner, pk, BannerForm, 'custom_admin/banner_form.html', 'panel_banner_list')


@login_required(login_url=LOGIN_URL)
def banner_delete(request, pk):
    return _delete_view(request, Banner, pk, 'custom_admin/banner_confirm_delete.html', 'panel_banner_list')


# =============================================================================
# Advantage
# =============================================================================

@login_required(login_url=LOGIN_URL)
def advantage_list(request):
    return _list_view(request, Advantage, 'custom_admin/advantage_list.html', 'advantages')


@login_required(login_url=LOGIN_URL)
def advantage_create(request):
    return _create_view(request, AdvantageForm, 'custom_admin/advantage_form.html', 'panel_advantage_list')


@login_required(login_url=LOGIN_URL)
def advantage_edit(request, pk):
    return _edit_view(request, Advantage, pk, AdvantageForm, 'custom_admin/advantage_form.html', 'panel_advantage_list')


@login_required(login_url=LOGIN_URL)
def advantage_delete(request, pk):
    return _delete_view(request, Advantage, pk, 'custom_admin/advantage_confirm_delete.html', 'panel_advantage_list')


# =============================================================================
# Statistic
# =============================================================================

@login_required(login_url=LOGIN_URL)
def statistic_list(request):
    return _list_view(request, Statistic, 'custom_admin/statistic_list.html', 'statistics')


@login_required(login_url=LOGIN_URL)
def statistic_create(request):
    return _create_view(request, StatisticForm, 'custom_admin/statistic_form.html', 'panel_statistic_list')


@login_required(login_url=LOGIN_URL)
def statistic_edit(request, pk):
    return _edit_view(request, Statistic, pk, StatisticForm, 'custom_admin/statistic_form.html', 'panel_statistic_list')


@login_required(login_url=LOGIN_URL)
def statistic_delete(request, pk):
    return _delete_view(request, Statistic, pk, 'custom_admin/statistic_confirm_delete.html', 'panel_statistic_list')


# =============================================================================
# Partner
# =============================================================================

@login_required(login_url=LOGIN_URL)
def partner_list(request):
    return _list_view(request, Partner, 'custom_admin/partner_list.html', 'partners')


@login_required(login_url=LOGIN_URL)
def partner_create(request):
    return _create_view(request, PartnerForm, 'custom_admin/partner_form.html', 'panel_partner_list')


@login_required(login_url=LOGIN_URL)
def partner_edit(request, pk):
    return _edit_view(request, Partner, pk, PartnerForm, 'custom_admin/partner_form.html', 'panel_partner_list')


@login_required(login_url=LOGIN_URL)
def partner_delete(request, pk):
    return _delete_view(request, Partner, pk, 'custom_admin/partner_confirm_delete.html', 'panel_partner_list')


# =============================================================================
# QualityPillar
# =============================================================================

@login_required(login_url=LOGIN_URL)
def qualitypillar_list(request):
    return _list_view(request, QualityPillar, 'custom_admin/qualitypillar_list.html', 'pillars')


@login_required(login_url=LOGIN_URL)
def qualitypillar_create(request):
    return _create_view(request, QualityPillarForm, 'custom_admin/qualitypillar_form.html', 'panel_qualitypillar_list')


@login_required(login_url=LOGIN_URL)
def qualitypillar_edit(request, pk):
    return _edit_view(request, QualityPillar, pk, QualityPillarForm, 'custom_admin/qualitypillar_form.html', 'panel_qualitypillar_list')


@login_required(login_url=LOGIN_URL)
def qualitypillar_delete(request, pk):
    return _delete_view(request, QualityPillar, pk, 'custom_admin/qualitypillar_confirm_delete.html', 'panel_qualitypillar_list')


# =============================================================================
# PageSeo
# =============================================================================

@login_required(login_url=LOGIN_URL)
def seo_list(request):
    return _list_view(request, PageSeo, 'custom_admin/seo_list.html', 'seo_entries')


@login_required(login_url=LOGIN_URL)
def seo_edit(request, pk):
    return _edit_view(request, PageSeo, pk, PageSeoForm, 'custom_admin/seo_form.html', 'panel_seo_list')


# =============================================================================
# Category
# =============================================================================

@login_required(login_url=LOGIN_URL)
def category_list(request):
    return _list_view(request, Category, 'custom_admin/category_list.html', 'categories')


@login_required(login_url=LOGIN_URL)
def category_create(request):
    return _create_view(request, CategoryForm, 'custom_admin/category_form.html', 'panel_category_list')


@login_required(login_url=LOGIN_URL)
def category_edit(request, pk):
    return _edit_view(request, Category, pk, CategoryForm, 'custom_admin/category_form.html', 'panel_category_list')


@login_required(login_url=LOGIN_URL)
def category_delete(request, pk):
    return _delete_view(request, Category, pk, 'custom_admin/category_confirm_delete.html', 'panel_category_list')


# =============================================================================
# Product (with ProductImage inline handling)
# =============================================================================

def _handle_product_images(request, product):
    """Handle multiple ProductImage uploads and deletions for a product."""
    images = request.FILES.getlist('images')
    for image in images:
        ProductImage.objects.create(product=product, image=image)
    delete_ids = request.POST.getlist('delete_images')
    if delete_ids:
        ProductImage.objects.filter(pk__in=delete_ids, product=product).delete()


@login_required(login_url=LOGIN_URL)
def product_list(request):
    return _list_view(request, Product, 'custom_admin/product_list.html', 'products')


@login_required(login_url=LOGIN_URL)
def product_create(request):
    return _create_view(
        request, ProductForm, 'custom_admin/product_form.html',
        'panel_product_list', extra_save=_handle_product_images,
    )


@login_required(login_url=LOGIN_URL)
def product_edit(request, pk):
    return _edit_view(
        request, Product, pk, ProductForm, 'custom_admin/product_form.html',
        'panel_product_list', extra_save=_handle_product_images,
    )


@login_required(login_url=LOGIN_URL)
def product_delete(request, pk):
    return _delete_view(request, Product, pk, 'custom_admin/product_confirm_delete.html', 'panel_product_list')


# =============================================================================
# Article
# =============================================================================

@login_required(login_url=LOGIN_URL)
def article_list(request):
    return _list_view(request, Article, 'custom_admin/article_list.html', 'articles')


@login_required(login_url=LOGIN_URL)
def article_create(request):
    return _create_view(request, ArticleForm, 'custom_admin/article_form.html', 'panel_article_list')


@login_required(login_url=LOGIN_URL)
def article_edit(request, pk):
    return _edit_view(request, Article, pk, ArticleForm, 'custom_admin/article_form.html', 'panel_article_list')


@login_required(login_url=LOGIN_URL)
def article_delete(request, pk):
    return _delete_view(request, Article, pk, 'custom_admin/article_confirm_delete.html', 'panel_article_list')


# =============================================================================
# Project (with ProjectImage inline handling)
# =============================================================================

def _handle_project_images(request, project):
    """Handle multiple ProjectImage uploads and deletions for a project."""
    images = request.FILES.getlist('images')
    for image in images:
        ProjectImage.objects.create(project=project, image=image)
    delete_ids = request.POST.getlist('delete_images')
    if delete_ids:
        ProjectImage.objects.filter(pk__in=delete_ids, project=project).delete()


@login_required(login_url=LOGIN_URL)
def project_list(request):
    return _list_view(request, Project, 'custom_admin/project_list.html', 'projects')


@login_required(login_url=LOGIN_URL)
def project_create(request):
    return _create_view(
        request, ProjectForm, 'custom_admin/project_form.html',
        'panel_project_list', extra_save=_handle_project_images,
    )


@login_required(login_url=LOGIN_URL)
def project_edit(request, pk):
    return _edit_view(
        request, Project, pk, ProjectForm, 'custom_admin/project_form.html',
        'panel_project_list', extra_save=_handle_project_images,
    )


@login_required(login_url=LOGIN_URL)
def project_delete(request, pk):
    return _delete_view(request, Project, pk, 'custom_admin/project_confirm_delete.html', 'panel_project_list')


# =============================================================================
# ContactRequest (read-only: list with filter + detail with auto-mark-read)
# =============================================================================

@login_required(login_url=LOGIN_URL)
def contact_list(request):
    qs = ContactRequest.objects.all().order_by('-id')
    filter_read = request.GET.get('is_read')
    if filter_read == '1':
        qs = qs.filter(is_read=True)
    elif filter_read == '0':
        qs = qs.filter(is_read=False)
    context = {
        'contacts': qs,
        'current_filter': filter_read,
    }
    return render(request, 'custom_admin/contact_list.html', context)


@login_required(login_url=LOGIN_URL)
def contact_detail(request, pk):
    obj = get_object_or_404(ContactRequest, pk=pk)
    if not obj.is_read:
        obj.is_read = True
        obj.save(update_fields=['is_read'])
    return render(request, 'custom_admin/contact_detail.html', {'contact': obj})
