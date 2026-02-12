from django.shortcuts import render, get_object_or_404
from core.models import PageSeo
from .models import Category, Product


def catalog(request):
    categories = Category.objects.all()
    try:
        page_seo = PageSeo.objects.get(page='catalog')
    except PageSeo.DoesNotExist:
        page_seo = None
    return render(request, 'catalog/catalog.html', {'categories': categories, 'page_seo': page_seo})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'catalog/category.html', {'category': category, 'products': products})


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, category__slug=category_slug)
    return render(request, 'catalog/product.html', {'product': product})
