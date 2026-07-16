from django.shortcuts import render, redirect
from django.contrib import messages

from products_brands_app.models import ProductCategory, Product, Brand
from .models import ContactEnquiry, BlogPost, HeroSlide, SolarSolution, Project, GalleryImage, Founder, AboutPage


def home(request):
    brands = Brand.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True).select_related('category')[:4]
    hero_slides = HeroSlide.objects.filter(is_active=True)
    solutions = SolarSolution.objects.filter(is_active=True)[:4]
    gallery_images = GalleryImage.objects.filter(is_active=True)
    context = {
        'brands': brands,
        'featured_products': featured_products,
        'hero_slides': hero_slides,
        'solutions': solutions,
        'gallery_images': gallery_images,
    }
    return render(request, 'index.html', context)


def about(request):
    founder = Founder.objects.first()
    about_page = AboutPage.objects.first()
    return render(request, 'about.html', {'founder': founder, 'about_page': about_page})


def services(request):
    solutions = SolarSolution.objects.filter(is_active=True)
    return render(request, 'services.html', {'solutions': solutions})


def products(request):
    """General products page on the main site, backed by products_brands_app models."""
    categories = ProductCategory.objects.all()
    brands = Brand.objects.filter(is_active=True)
    selected_category_slug = request.GET.get('category')

    if selected_category_slug:
        selected_category = categories.filter(slug=selected_category_slug).first()
        products_qs = Product.objects.filter(category=selected_category, is_active=True) if selected_category else Product.objects.none()
    else:
        selected_category = None
        products_qs = Product.objects.filter(is_active=True).select_related('category')

    context = {
        'categories': categories,
        'products': products_qs,
        'brands': brands,
        'selected_category': selected_category,
    }
    return render(request, 'products.html', context)


def projects(request):
    project_list = Project.objects.filter(is_active=True)
    return render(request, 'projects.html', {'projects': project_list})


def calculator(request):
    return render(request, 'calculator.html')


def blog(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'blog.html', {'posts': posts})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        service = request.POST.get('service', '').strip()
        message = request.POST.get('message', '').strip()

        if name and phone and message:
            ContactEnquiry.objects.create(
                name=name, phone=phone, email=email,
                service=service, message=message,
            )
            messages.success(request, 'Thank you! Your enquiry has been submitted. We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'contact.html')
