from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('projects/', views.projects, name='projects'),
    path('calculator/', views.calculator, name='calculator'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
]
