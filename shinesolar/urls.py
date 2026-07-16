from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('website.admin_urls')),
    path('products/', include('products_brands_app.urls')),
    path('', include('website.urls')),
]

# NOTE: Django's `django.conf.urls.static.static()` helper only serves
# MEDIA files when DEBUG=True. This project runs with DEBUG=False (even
# in local/preview use), so that helper silently returns an empty
# urlpatterns list and every uploaded image (products, brands, solutions,
# gallery, founder photo) 404s. We serve /media/ explicitly here instead.
# For a real production deployment with real traffic, swap this out for
# a proper media host (e.g. S3, Cloudinary, or your web server / Nginx
# serving /media/ directly) instead of Django serving it.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
