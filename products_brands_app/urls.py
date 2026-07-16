from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.products_and_brands, name='products_and_brands'),
    path('category/<slug:slug>/', views.product_category, name='product_category'),
]
