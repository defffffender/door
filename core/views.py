from django.shortcuts import render, redirect
from django.utils import translation
from django.conf import settings
from .models import Banner, Advantage, Statistic, Partner, QualityPillar, SiteSettings, PageSeo
from catalog.models import Category, Product
from portfolio.models import Project


def _get_page_seo(page_key):
    try:
        return PageSeo.objects.get(page=page_key)
    except PageSeo.DoesNotExist:
        return None


def home(request):
    context = {
        'banners': Banner.objects.filter(is_active=True),
        'popular_products': Product.objects.filter(is_popular=True)[:8],
        'categories': Category.objects.all(),
        'advantages': Advantage.objects.all(),
        'statistics': Statistic.objects.all(),
        'partners': Partner.objects.all(),
        'quality_pillars': QualityPillar.objects.all(),
        'projects': Project.objects.all()[:4],
        'page_seo': _get_page_seo('home'),
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'advantages': Advantage.objects.all(),
        'statistics': Statistic.objects.all(),
        'quality_pillars': QualityPillar.objects.all(),
        'partners': Partner.objects.all(),
        'page_seo': _get_page_seo('about'),
    }
    return render(request, 'core/about.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def switch_language(request, lang_code):
    if lang_code not in dict(settings.LANGUAGES):
        lang_code = settings.LANGUAGE_CODE

    next_url = request.GET.get('next', '/')

    # Strip existing language prefix from path
    for code, _ in settings.LANGUAGES:
        prefix = f'/{code}/'
        if next_url.startswith(prefix):
            next_url = next_url[len(prefix) - 1:]
            break

    # Add new language prefix (skip for default language)
    if lang_code == settings.LANGUAGE_CODE:
        redirect_url = next_url
    else:
        redirect_url = f'/{lang_code}{next_url}'

    response = redirect(redirect_url)
    response.set_cookie(
        settings.LANGUAGE_COOKIE_NAME,
        lang_code,
        max_age=365 * 24 * 60 * 60,
        path='/',
    )
    return response
