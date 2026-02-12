from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='panel_dashboard'),
    path('login/', views.login_view, name='panel_login'),
    path('logout/', views.logout_view, name='panel_logout'),

    # Site Settings (singleton)
    path('settings/', views.settings_edit, name='panel_settings'),

    # SEO
    path('seo/', views.seo_list, name='panel_seo_list'),
    path('seo/<int:pk>/edit/', views.seo_edit, name='panel_seo_edit'),

    # Banners
    path('banners/', views.banner_list, name='panel_banner_list'),
    path('banners/create/', views.banner_create, name='panel_banner_create'),
    path('banners/<int:pk>/edit/', views.banner_edit, name='panel_banner_edit'),
    path('banners/<int:pk>/delete/', views.banner_delete, name='panel_banner_delete'),

    # Advantages
    path('advantages/', views.advantage_list, name='panel_advantage_list'),
    path('advantages/create/', views.advantage_create, name='panel_advantage_create'),
    path('advantages/<int:pk>/edit/', views.advantage_edit, name='panel_advantage_edit'),
    path('advantages/<int:pk>/delete/', views.advantage_delete, name='panel_advantage_delete'),

    # Statistics
    path('statistics/', views.statistic_list, name='panel_statistic_list'),
    path('statistics/create/', views.statistic_create, name='panel_statistic_create'),
    path('statistics/<int:pk>/edit/', views.statistic_edit, name='panel_statistic_edit'),
    path('statistics/<int:pk>/delete/', views.statistic_delete, name='panel_statistic_delete'),

    # Partners
    path('partners/', views.partner_list, name='panel_partner_list'),
    path('partners/create/', views.partner_create, name='panel_partner_create'),
    path('partners/<int:pk>/edit/', views.partner_edit, name='panel_partner_edit'),
    path('partners/<int:pk>/delete/', views.partner_delete, name='panel_partner_delete'),

    # Quality Pillars
    path('pillars/', views.qualitypillar_list, name='panel_qualitypillar_list'),
    path('pillars/create/', views.qualitypillar_create, name='panel_qualitypillar_create'),
    path('pillars/<int:pk>/edit/', views.qualitypillar_edit, name='panel_qualitypillar_edit'),
    path('pillars/<int:pk>/delete/', views.qualitypillar_delete, name='panel_qualitypillar_delete'),

    # Categories
    path('categories/', views.category_list, name='panel_category_list'),
    path('categories/create/', views.category_create, name='panel_category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='panel_category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='panel_category_delete'),

    # Products
    path('products/', views.product_list, name='panel_product_list'),
    path('products/create/', views.product_create, name='panel_product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='panel_product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='panel_product_delete'),

    # Articles
    path('articles/', views.article_list, name='panel_article_list'),
    path('articles/create/', views.article_create, name='panel_article_create'),
    path('articles/<int:pk>/edit/', views.article_edit, name='panel_article_edit'),
    path('articles/<int:pk>/delete/', views.article_delete, name='panel_article_delete'),

    # Projects
    path('projects/', views.project_list, name='panel_project_list'),
    path('projects/create/', views.project_create, name='panel_project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='panel_project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='panel_project_delete'),

    # Contact Requests
    path('contacts/', views.contact_list, name='panel_contacts'),
    path('contacts/<int:pk>/', views.contact_detail, name='panel_contact_detail'),
]
