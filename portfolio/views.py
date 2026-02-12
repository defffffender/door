from django.shortcuts import render, get_object_or_404
from core.models import PageSeo
from .models import Project


def portfolio_list(request):
    projects = Project.objects.all()
    try:
        page_seo = PageSeo.objects.get(page='portfolio')
    except PageSeo.DoesNotExist:
        page_seo = None
    return render(request, 'portfolio/list.html', {'projects': projects, 'page_seo': page_seo})


def portfolio_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/detail.html', {'project': project})
