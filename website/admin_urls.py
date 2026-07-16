from django.urls import path
from . import admin_views

urlpatterns = [
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    # Products
    path('products/', admin_views.admin_products, name='admin_products'),
    path('products/add/', admin_views.admin_product_add, name='admin_product_add'),
    path('products/<int:pk>/edit/', admin_views.admin_product_edit, name='admin_product_edit'),
    path('products/<int:pk>/delete/', admin_views.admin_product_delete, name='admin_product_delete'),
    # Brands
    path('brands/', admin_views.admin_brands, name='admin_brands'),
    path('brands/add/', admin_views.admin_brand_add, name='admin_brand_add'),
    path('brands/<int:pk>/edit/', admin_views.admin_brand_edit, name='admin_brand_edit'),
    path('brands/<int:pk>/delete/', admin_views.admin_brand_delete, name='admin_brand_delete'),
    # Hero Slider
    path('hero-slides/', admin_views.admin_hero_slides, name='admin_hero_slides'),
    path('hero-slides/add/', admin_views.admin_hero_slide_add, name='admin_hero_slide_add'),
    path('hero-slides/<int:pk>/edit/', admin_views.admin_hero_slide_edit, name='admin_hero_slide_edit'),
    path('hero-slides/<int:pk>/delete/', admin_views.admin_hero_slide_delete, name='admin_hero_slide_delete'),
    # Solar Solutions
    path('solutions/', admin_views.admin_solutions, name='admin_solutions'),
    path('solutions/add/', admin_views.admin_solution_add, name='admin_solution_add'),
    path('solutions/<int:pk>/edit/', admin_views.admin_solution_edit, name='admin_solution_edit'),
    path('solutions/<int:pk>/delete/', admin_views.admin_solution_delete, name='admin_solution_delete'),
    # Projects
    path('projects/', admin_views.admin_projects, name='admin_projects'),
    path('projects/add/', admin_views.admin_project_add, name='admin_project_add'),
    path('projects/<int:pk>/edit/', admin_views.admin_project_edit, name='admin_project_edit'),
    path('projects/<int:pk>/delete/', admin_views.admin_project_delete, name='admin_project_delete'),
    # Gallery
    path('gallery/', admin_views.admin_gallery, name='admin_gallery'),
    path('gallery/add/', admin_views.admin_gallery_add, name='admin_gallery_add'),
    path('gallery/<int:pk>/edit/', admin_views.admin_gallery_edit, name='admin_gallery_edit'),
    path('gallery/<int:pk>/delete/', admin_views.admin_gallery_delete, name='admin_gallery_delete'),
    # Contacts
    path('contacts/', admin_views.admin_contacts, name='admin_contacts'),
    # Blog
    path('blog/', admin_views.admin_blog, name='admin_blog'),
    path('blog/add/', admin_views.admin_blog_add, name='admin_blog_add'),
    path('blog/<int:pk>/edit/', admin_views.admin_blog_edit, name='admin_blog_edit'),
    path('blog/<int:pk>/delete/', admin_views.admin_blog_delete, name='admin_blog_delete'),
    # Founder
    path('founder/edit/', admin_views.admin_founder_edit, name='admin_founder_edit'),
    path('about/edit/', admin_views.admin_about_edit, name='admin_about_edit'),
]
