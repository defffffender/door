from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings
from .models import Banner, Advantage, Statistic, Partner, QualityPillar, SiteSettings, PageSeo
from catalog.models import Category, Product
from news.models import Article
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


def robots_txt(request):
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /panel/

Sitemap: https://staeldi.uz/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


def sitemap_xml(request):
    site_url = 'https://staeldi.uz'
    urls = [
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        {'loc': '/about/', 'priority': '0.8', 'changefreq': 'monthly'},
        {'loc': '/catalog/', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': '/news/', 'priority': '0.7', 'changefreq': 'weekly'},
        {'loc': '/portfolio/', 'priority': '0.7', 'changefreq': 'monthly'},
        {'loc': '/contacts/', 'priority': '0.8', 'changefreq': 'monthly'},
    ]

    # Add categories
    for cat in Category.objects.all():
        urls.append({'loc': f'/catalog/{cat.slug}/', 'priority': '0.8', 'changefreq': 'weekly'})

    # Add products
    for product in Product.objects.all():
        urls.append({'loc': f'/catalog/{product.category.slug}/{product.slug}/', 'priority': '0.7', 'changefreq': 'weekly'})

    # Add articles
    for article in Article.objects.filter(is_published=True):
        urls.append({'loc': f'/news/{article.slug}/', 'priority': '0.6', 'changefreq': 'monthly'})

    # Add portfolio projects
    for project in Project.objects.all():
        urls.append({'loc': f'/portfolio/{project.slug}/', 'priority': '0.6', 'changefreq': 'monthly'})

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f'  <url>\n'
        xml += f'    <loc>{site_url}{u["loc"]}</loc>\n'
        xml += f'    <changefreq>{u["changefreq"]}</changefreq>\n'
        xml += f'    <priority>{u["priority"]}</priority>\n'
        xml += f'  </url>\n'
    xml += '</urlset>'

    return HttpResponse(xml, content_type='application/xml')


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
