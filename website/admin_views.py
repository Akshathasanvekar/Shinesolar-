from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from products_brands_app.models import ProductCategory, Product, Brand
from .models import ContactEnquiry, BlogPost, HeroSlide, SolarSolution, Project, GalleryImage, Founder, AboutPage


def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')

    # Pull homepage banner (hero slide) images and services (solar solution)
    # images to power the rotating background on the login page.
    banner_images = [
        slide.display_image_url for slide in HeroSlide.objects.filter(is_active=True)
        if slide.display_image_url
    ]
    service_images = [
        sol.display_image_url for sol in SolarSolution.objects.filter(is_active=True)
        if sol.display_image_url
    ]
    login_bg_images = banner_images + service_images
    if not login_bg_images:
        # Same default fallback photos used on the homepage hero banner.
        login_bg_images = [
            'https://images.unsplash.com/photo-1509391366360-2e959784a276?fm=jpg&q=80&w=1600&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1613665813446-82a78c468a1d?fm=jpg&q=80&w=1600&auto=format&fit=crop',
            'https://images.unsplash.com/photo-1655300256335-beef51a914fe?fm=jpg&q=80&w=1600&auto=format&fit=crop',
        ]
    return render(request, 'admin_panel/login.html', {'login_bg_images': login_bg_images})


def admin_logout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    context = {
        'product_count': Product.objects.count(),
        'brand_count': Brand.objects.count(),
        'contact_count': ContactEnquiry.objects.count(),
        'category_count': ProductCategory.objects.count(),
        'blog_count': BlogPost.objects.count(),
        'hero_slide_count': HeroSlide.objects.count(),
        'solution_count': SolarSolution.objects.count(),
        'project_count': Project.objects.count(),
        'gallery_count': GalleryImage.objects.count(),
        'recent_products': Product.objects.select_related('category').order_by('-id')[:8],
        'recent_contacts': ContactEnquiry.objects.order_by('-created_at')[:8],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# --- PRODUCTS ---
@login_required(login_url='/admin-panel/login/')
def admin_products(request):
    if not request.user.is_staff:
        return redirect('home')
    products = Product.objects.select_related('category').all()
    return render(request, 'admin_panel/products.html', {'products': products})


@login_required(login_url='/admin-panel/login/')
def admin_product_add(request):
    if not request.user.is_staff:
        return redirect('home')
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        cat_id = request.POST.get('category')
        description = request.POST.get('description', '')
        order = int(request.POST.get('order', 0))
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        if name and cat_id and image:
            category = get_object_or_404(ProductCategory, id=cat_id)
            slug = slugify(name)
            # ensure unique slug within category
            base_slug = slug
            counter = 1
            while Product.objects.filter(category=category, slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            Product.objects.create(
                name=name, category=category, slug=slug,
                description=description, order=order,
                is_active=is_active, image=image
            )
            messages.success(request, f'Product "{name}" added successfully!')
            return redirect('admin_products')
        else:
            messages.error(request, 'Please fill all required fields.')
    return render(request, 'admin_panel/product_form.html', {'categories': categories})


@login_required(login_url='/admin-panel/login/')
def admin_product_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=pk)
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name', product.name).strip()
        cat_id = request.POST.get('category')
        if cat_id:
            product.category = get_object_or_404(ProductCategory, id=cat_id)
        product.description = request.POST.get('description', '')
        product.order = int(request.POST.get('order', 0))
        product.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        messages.success(request, f'Product "{product.name}" updated!')
        return redirect('admin_products')
    return render(request, 'admin_panel/product_form.html', {'product': product, 'categories': categories})


@login_required(login_url='/admin-panel/login/')
def admin_product_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    product = get_object_or_404(Product, id=pk)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('admin_products')


# --- BRANDS ---
@login_required(login_url='/admin-panel/login/')
def admin_brands(request):
    if not request.user.is_staff:
        return redirect('home')
    brands = Brand.objects.all()
    return render(request, 'admin_panel/brands.html', {'brands': brands})


@login_required(login_url='/admin-panel/login/')
def admin_brand_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        website = request.POST.get('website', '')
        order = int(request.POST.get('order', 0))
        is_active = 'is_active' in request.POST
        logo = request.FILES.get('logo')
        if name and logo:
            slug = slugify(name)
            base_slug = slug
            counter = 1
            while Brand.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            Brand.objects.create(name=name, slug=slug, website=website, order=order, is_active=is_active, logo=logo)
            messages.success(request, f'Brand "{name}" added!')
            return redirect('admin_brands')
        else:
            messages.error(request, 'Please fill all required fields.')
    return render(request, 'admin_panel/brand_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_brand_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    brand = get_object_or_404(Brand, id=pk)
    if request.method == 'POST':
        brand.name = request.POST.get('name', brand.name).strip()
        brand.website = request.POST.get('website', '')
        brand.order = int(request.POST.get('order', 0))
        brand.is_active = 'is_active' in request.POST
        if request.FILES.get('logo'):
            brand.logo = request.FILES['logo']
        brand.save()
        messages.success(request, f'Brand "{brand.name}" updated!')
        return redirect('admin_brands')
    return render(request, 'admin_panel/brand_form.html', {'brand': brand})


@login_required(login_url='/admin-panel/login/')
def admin_brand_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    brand = get_object_or_404(Brand, id=pk)
    brand.delete()
    messages.success(request, 'Brand deleted.')
    return redirect('admin_brands')


# --- HERO SLIDES ---
@login_required(login_url='/admin-panel/login/')
def admin_hero_slides(request):
    if not request.user.is_staff:
        return redirect('home')
    slides = HeroSlide.objects.all()
    return render(request, 'admin_panel/hero_slides.html', {'slides': slides})


@login_required(login_url='/admin-panel/login/')
def admin_hero_slide_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url', '').strip()
        if image or image_url:
            HeroSlide.objects.create(
                title=title, order=order, is_active=is_active,
                image=image, image_url=image_url,
            )
            messages.success(request, 'Hero slide added!')
            return redirect('admin_hero_slides')
        else:
            messages.error(request, 'Please choose an image or provide a photo link for the slide.')
    return render(request, 'admin_panel/hero_slide_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_hero_slide_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    slide = get_object_or_404(HeroSlide, id=pk)
    if request.method == 'POST':
        slide.title = request.POST.get('title', slide.title).strip()
        slide.order = int(request.POST.get('order', 0) or 0)
        slide.is_active = 'is_active' in request.POST
        slide.image_url = request.POST.get('image_url', '').strip()
        if request.FILES.get('image'):
            slide.image = request.FILES['image']
        slide.save()
        messages.success(request, 'Hero slide updated!')
        return redirect('admin_hero_slides')
    return render(request, 'admin_panel/hero_slide_form.html', {'slide': slide})


@login_required(login_url='/admin-panel/login/')
def admin_hero_slide_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    slide = get_object_or_404(HeroSlide, id=pk)
    slide.delete()
    messages.success(request, 'Hero slide deleted.')
    return redirect('admin_hero_slides')


# --- SOLAR SOLUTIONS (services page cards) ---
@login_required(login_url='/admin-panel/login/')
def admin_solutions(request):
    if not request.user.is_staff:
        return redirect('home')
    solutions = SolarSolution.objects.all()
    return render(request, 'admin_panel/solutions.html', {'solutions': solutions})


@login_required(login_url='/admin-panel/login/')
def admin_solution_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        icon_class = request.POST.get('icon_class', '').strip() or 'fa-solid fa-solar-panel'
        image_url = request.POST.get('image_url', '').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        if title and description:
            SolarSolution.objects.create(
                title=title, description=description, icon_class=icon_class,
                order=order, is_active=is_active, image=image, image_url=image_url
            )
            messages.success(request, f'Solution "{title}" added!')
            return redirect('admin_solutions')
        else:
            messages.error(request, 'Title and description are required.')
    return render(request, 'admin_panel/solution_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_solution_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    solution = get_object_or_404(SolarSolution, id=pk)
    if request.method == 'POST':
        solution.title = request.POST.get('title', solution.title).strip()
        solution.description = request.POST.get('description', solution.description).strip()
        solution.icon_class = request.POST.get('icon_class', solution.icon_class).strip() or solution.icon_class
        solution.image_url = request.POST.get('image_url', solution.image_url).strip()
        solution.order = int(request.POST.get('order', 0) or 0)
        solution.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            solution.image = request.FILES['image']
        solution.save()
        messages.success(request, f'Solution "{solution.title}" updated!')
        return redirect('admin_solutions')
    return render(request, 'admin_panel/solution_form.html', {'solution': solution})


@login_required(login_url='/admin-panel/login/')
def admin_solution_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    solution = get_object_or_404(SolarSolution, id=pk)
    solution.delete()
    messages.success(request, 'Solution deleted.')
    return redirect('admin_solutions')


# --- PROJECTS (projects page cards) ---
@login_required(login_url='/admin-panel/login/')
def admin_projects(request):
    if not request.user.is_staff:
        return redirect('home')
    projects = Project.objects.all()
    return render(request, 'admin_panel/projects.html', {'projects': projects})


@login_required(login_url='/admin-panel/login/')
def admin_project_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        icon_class = request.POST.get('icon_class', '').strip() or 'fa-solid fa-solar-panel'
        image_url = request.POST.get('image_url', '').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        if title and description:
            Project.objects.create(
                title=title, description=description, icon_class=icon_class,
                order=order, is_active=is_active, image=image, image_url=image_url
            )
            messages.success(request, f'Project "{title}" added!')
            return redirect('admin_projects')
        else:
            messages.error(request, 'Title and description are required.')
    return render(request, 'admin_panel/project_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_project_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    project = get_object_or_404(Project, id=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title', project.title).strip()
        project.description = request.POST.get('description', project.description).strip()
        project.icon_class = request.POST.get('icon_class', project.icon_class).strip() or project.icon_class
        project.image_url = request.POST.get('image_url', project.image_url).strip()
        project.order = int(request.POST.get('order', 0) or 0)
        project.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            project.image = request.FILES['image']
        project.save()
        messages.success(request, f'Project "{project.title}" updated!')
        return redirect('admin_projects')
    return render(request, 'admin_panel/project_form.html', {'project': project})


@login_required(login_url='/admin-panel/login/')
def admin_project_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    project = get_object_or_404(Project, id=pk)
    project.delete()
    messages.success(request, 'Project deleted.')
    return redirect('admin_projects')


# --- GALLERY (homepage Solar Installations Gallery) ---
@login_required(login_url='/admin-panel/login/')
def admin_gallery(request):
    if not request.user.is_staff:
        return redirect('home')
    images = GalleryImage.objects.all()
    return render(request, 'admin_panel/gallery.html', {'images': images})


@login_required(login_url='/admin-panel/login/')
def admin_gallery_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        subtitle = request.POST.get('subtitle', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        order = int(request.POST.get('order', 0) or 0)
        is_active = 'is_active' in request.POST
        image = request.FILES.get('image')
        if title and (image or image_url):
            GalleryImage.objects.create(
                title=title, subtitle=subtitle,
                order=order, is_active=is_active, image=image, image_url=image_url
            )
            messages.success(request, f'Gallery image "{title}" added!')
            return redirect('admin_gallery')
        else:
            messages.error(request, 'Title and a photo (upload or link) are required.')
    return render(request, 'admin_panel/gallery_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_gallery_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    image_obj = get_object_or_404(GalleryImage, id=pk)
    if request.method == 'POST':
        image_obj.title = request.POST.get('title', image_obj.title).strip()
        image_obj.subtitle = request.POST.get('subtitle', image_obj.subtitle).strip()
        image_obj.image_url = request.POST.get('image_url', image_obj.image_url).strip()
        image_obj.order = int(request.POST.get('order', 0) or 0)
        image_obj.is_active = 'is_active' in request.POST
        if request.FILES.get('image'):
            image_obj.image = request.FILES['image']
        image_obj.save()
        messages.success(request, f'Gallery image "{image_obj.title}" updated!')
        return redirect('admin_gallery')
    return render(request, 'admin_panel/gallery_form.html', {'image_obj': image_obj})


@login_required(login_url='/admin-panel/login/')
def admin_gallery_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    image_obj = get_object_or_404(GalleryImage, id=pk)
    image_obj.delete()
    messages.success(request, 'Gallery image deleted.')
    return redirect('admin_gallery')


# --- CONTACTS ---
@login_required(login_url='/admin-panel/login/')
def admin_contacts(request):
    if not request.user.is_staff:
        return redirect('home')
    contacts = ContactEnquiry.objects.all()
    return render(request, 'admin_panel/contacts.html', {'contacts': contacts})


# --- BLOG ---
@login_required(login_url='/admin-panel/login/')
def admin_blog(request):
    if not request.user.is_staff:
        return redirect('home')
    posts = BlogPost.objects.all()
    return render(request, 'admin_panel/blog.html', {'posts': posts})


@login_required(login_url='/admin-panel/login/')
def admin_blog_add(request):
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        excerpt = request.POST.get('excerpt', '')
        content = request.POST.get('content', '')
        is_published = 'is_published' in request.POST
        image = request.FILES.get('image')
        image_url = request.POST.get('image_url', '').strip()
        if title and content:
            slug = slugify(title)
            base_slug = slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            post = BlogPost.objects.create(
                title=title, slug=slug, excerpt=excerpt,
                content=content, is_published=is_published, image_url=image_url
            )
            if image:
                post.image = image
                post.save()
            messages.success(request, f'Blog post "{title}" created!')
            return redirect('admin_blog')
        else:
            messages.error(request, 'Title and content are required.')
    return render(request, 'admin_panel/blog_form.html', {})


@login_required(login_url='/admin-panel/login/')
def admin_blog_edit(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    post = get_object_or_404(BlogPost, id=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title).strip()
        post.excerpt = request.POST.get('excerpt', '')
        post.content = request.POST.get('content', '')
        post.is_published = 'is_published' in request.POST
        post.image_url = request.POST.get('image_url', post.image_url).strip()
        if request.FILES.get('image'):
            post.image = request.FILES['image']
        post.save()
        messages.success(request, f'Blog post "{post.title}" updated!')
        return redirect('admin_blog')
    return render(request, 'admin_panel/blog_form.html', {'post': post})


@login_required(login_url='/admin-panel/login/')
def admin_blog_delete(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    post = get_object_or_404(BlogPost, id=pk)
    post.delete()
    messages.success(request, 'Blog post deleted.')
    return redirect('admin_blog')


@login_required(login_url='/admin-panel/login/')
def admin_founder_edit(request):
    if not request.user.is_staff:
        return redirect('home')
    
    founder = Founder.objects.first()
    if not founder:
        founder = Founder.objects.create(
            name="Mr. Owner Name",
            role="Owner, Founder & Director",
            bio="With a passion for renewable energy and innovation, Mr. Owner Name started Shine Solar Energy with a vision to provide dependable solar solutions.",
            skills="Solar Energy Solutions\nProject Management\nCustomer Service\nRenewable Energy Development"
        )
    
    if request.method == 'POST':
        founder.name = request.POST.get('name', '').strip()
        founder.role = request.POST.get('role', '').strip()
        founder.bio = request.POST.get('bio', '').strip()
        founder.skills = request.POST.get('skills', '').strip()
        
        if request.FILES.get('image'):
            founder.image = request.FILES['image']
            
        founder.save()
        messages.success(request, 'Founder/Owner details updated successfully!')
        return redirect('admin_dashboard')
        
    return render(request, 'admin_panel/founder_form.html', {'founder': founder})


@login_required(login_url='/admin-panel/login/')
def admin_about_edit(request):
    if not request.user.is_staff:
        return redirect('home')

    about = AboutPage.objects.first()
    if not about:
        about = AboutPage.objects.create()

    if request.method == 'POST':
        about.intro_image_url = request.POST.get('intro_image_url', about.intro_image_url).strip()

        if request.FILES.get('intro_image'):
            about.intro_image = request.FILES['intro_image']

        about.save()
        messages.success(request, 'About page images updated successfully!')
        return redirect('admin_about_edit')

    return render(request, 'admin_panel/about_form.html', {'about': about})


