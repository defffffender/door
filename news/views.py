from django.shortcuts import render, get_object_or_404
from core.models import PageSeo
from .models import Article


def news_list(request):
    articles = Article.objects.filter(is_published=True)
    try:
        page_seo = PageSeo.objects.get(page='news')
    except PageSeo.DoesNotExist:
        page_seo = None
    return render(request, 'news/list.html', {'articles': articles, 'page_seo': page_seo})


def news_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, 'news/detail.html', {'article': article})
