from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product, Brand


def products_and_brands(request):
    """Main page showing all product categories and brands."""
    categories = ProductCategory.objects.prefetch_related('products').all()
    brands = Brand.objects.filter(is_active=True)
    selected_category_slug = request.GET.get('category')

    if selected_category_slug:
        selected_category = get_object_or_404(ProductCategory, slug=selected_category_slug)
        products = Product.objects.filter(category=selected_category, is_active=True)
    else:
        selected_category = None
        products = Product.objects.filter(is_active=True).select_related('category')

    context = {
        'categories': categories,
        'products': products,
        'brands': brands,
        'selected_category': selected_category,
    }
    return render(request, 'products/products_and_brands.html', context)


def product_category(request, slug):
    """View products filtered by a specific category."""
    category = get_object_or_404(ProductCategory, slug=slug)
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(category=category, is_active=True)
    brands = Brand.objects.filter(is_active=True)

    context = {
        'categories': categories,
        'products': products,
        'brands': brands,
        'selected_category': category,
    }
    return render(request, 'products/products_and_brands.html', context)
