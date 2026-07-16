from django.db import models


class HeroSlide(models.Model):
    title = models.CharField(max_length=200, blank=True, help_text='Optional heading override for this slide')
    image = models.ImageField(upload_to='hero_slides/', blank=True, null=True, help_text='Uploading here always overrides the link below.')
    image_url = models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above (e.g. a temporary stock photo link).')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.title or f"Hero Slide {self.pk}"

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url


class SolarSolution(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=300)
    icon_class = models.CharField(
        max_length=100, default='fa-solid fa-solar-panel',
        help_text="Font Awesome icon class shown on the badge, e.g. 'fa-solid fa-house'"
    )
    image = models.ImageField(upload_to='solutions/', blank=True, null=True, help_text='Photo shown at the top of the card. Uploading here always overrides the link below.')
    image_url = models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above (e.g. a temporary stock photo link).')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Solar Solutions'

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url


class Project(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Residential Project")
    description = models.CharField(max_length=300, help_text="e.g. 5KW Rooftop Solar Installation.")
    icon_class = models.CharField(
        max_length=100, default='fa-solid fa-solar-panel',
        help_text="Font Awesome icon class shown on the badge, e.g. 'fa-solid fa-house'"
    )
    image = models.ImageField(upload_to='projects/', blank=True, null=True, help_text='Photo shown on the card. Uploading here always overrides the link below.')
    image_url = models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above (e.g. a temporary stock photo link).')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. Rooftop Array")
    subtitle = models.CharField(max_length=200, blank=True, help_text="e.g. Residential Installation")
    image = models.ImageField(upload_to='gallery/', blank=True, null=True, help_text='Uploading here always overrides the link below.')
    image_url = models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above (e.g. a temporary stock photo link).')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url


class ContactEnquiry(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    service = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact Enquiries'

    def __str__(self):
        return f"{self.name} - {self.phone}"


class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True)
    excerpt = models.TextField(max_length=400, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True, help_text='Uploading here always overrides the link below.')
    image_url = models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above (e.g. a temporary stock photo link).')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    @property
    def display_image_url(self):
        if self.image:
            return self.image.url
        return self.image_url


class AboutPage(models.Model):
    """Singleton holding the editable images used on the About Us page."""
    intro_image = models.ImageField(
        upload_to='about/', blank=True, null=True,
        help_text='Photo shown next to "Who We Are" at the top of the About page. Uploading here always overrides the link below.'
    )
    intro_image_url = models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above.')

    gallery_image_1 = models.ImageField(upload_to='about/', blank=True, null=True, help_text='1st photo in the Projects Gallery strip.')
    gallery_image_1_url = models.URLField(blank=True, default='')

    gallery_image_2 = models.ImageField(upload_to='about/', blank=True, null=True, help_text='2nd photo in the Projects Gallery strip.')
    gallery_image_2_url = models.URLField(blank=True, default='')

    gallery_image_3 = models.ImageField(upload_to='about/', blank=True, null=True, help_text='3rd photo in the Projects Gallery strip.')
    gallery_image_3_url = models.URLField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'About Page'

    def __str__(self):
        return 'About Page Images'

    @property
    def display_intro_image_url(self):
        if self.intro_image:
            return self.intro_image.url
        return self.intro_image_url

    @property
    def display_gallery_image_1(self):
        if self.gallery_image_1:
            return self.gallery_image_1.url
        return self.gallery_image_1_url

    @property
    def display_gallery_image_2(self):
        if self.gallery_image_2:
            return self.gallery_image_2.url
        return self.gallery_image_2_url

    @property
    def display_gallery_image_3(self):
        if self.gallery_image_3:
            return self.gallery_image_3.url
        return self.gallery_image_3_url


class Founder(models.Model):
    name = models.CharField(max_length=200, default='Mr. Owner Name')
    role = models.CharField(max_length=200, default='Owner, Founder & Director')
    image = models.ImageField(upload_to='founder/', blank=True, null=True)
    bio = models.TextField(
        default='With a passion for renewable energy and innovation, Mr. Owner Name started Shine Solar Energy with a vision to provide dependable solar solutions.'
    )
    skills = models.TextField(
        default="Solar Energy Solutions\nProject Management\nCustomer Service\nRenewable Energy Development",
        help_text='Enter one skill per line'
    )

    class Meta:
        verbose_name_plural = 'Founder Details'

    def __str__(self):
        return self.name

    def get_skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split('\n') if s.strip()]
        return []
