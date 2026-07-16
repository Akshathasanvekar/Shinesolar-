from django.contrib import admin
from .models import ContactEnquiry, HeroSlide, SolarSolution, Project, GalleryImage


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'service', 'created_at')
    list_filter = ('service', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')


@admin.register(SolarSolution)
class SolarSolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'id')
