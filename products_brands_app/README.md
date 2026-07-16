# Products & Brands — Django App Integration Guide

## Folder Structure

```
products_brands_app/
├── __init__.py
├── apps.py
├── models.py          ← ProductCategory, Product, Brand
├── views.py
├── urls.py
├── admin.py
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
├── templates/
│   └── products/
│       └── products_and_brands.html
└── management/
    └── commands/
        └── seed_products_brands.py   ← one-time data loader
```

---

## Step 1 — Copy the app into your project

```
cp -r products_brands_app/  <your_project_root>/
```

---

## Step 2 — settings.py

```python
INSTALLED_APPS = [
    ...
    'products_brands_app',   # ← add this
]

# Make sure these are set:
import os
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

## Step 3 — urls.py (project-level)

```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    ...
    path('products/', include('products_brands_app.urls', namespace='products')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Step 4 — Run migrations

```bash
python manage.py migrate
```

---

## Step 5 — Copy image assets

Place the **"products and brands"** folder (from your zip) inside a folder
called `assets/` next to `manage.py`:

```
your_project/
├── manage.py
├── assets/
│   └── products and brands/
│       ├── EV Charging Solutions/
│       ├── Selling Brands/
│       ├── Solar Panels/
│       └── ...
```

---

## Step 6 — Seed the database

```bash
python manage.py seed_products_brands
```

This command:
- Copies all product images → `media/products/`
- Copies all brand logos  → `media/brands/`
- Creates `ProductCategory`, `Product`, and `Brand` records

Re-run any time to update (safe to run multiple times — uses update_or_create).

To reset and reseed from scratch:
```bash
python manage.py seed_products_brands --clear
```

---

## Step 7 — Add a nav link in your base template

```html
<a href="{% url 'products:products_and_brands' %}">Products</a>
```

---

## Step 8 — Install Pillow (if not already)

```bash
pip install Pillow
```

---

## Admin

Visit `/admin/` → you'll see:
- **Product Categories** — reorder, add icons
- **Products** — per-category listing, toggle active
- **Brands** — reorder, toggle active

---

## URLs produced

| URL                                        | View                |
|--------------------------------------------|---------------------|
| `/products/`                               | All products + brands |
| `/products/?category=solar-panels`         | Filtered by category (query param) |
| `/products/category/solar-panels/`         | Filtered by category (clean URL) |

---

## Template block requirements

Your `base.html` must define:
- `{% block extra_css %}` — for page styles
- `{% block content %}` — for page body
- `{% block extra_js %}` — for scripts

FontAwesome 6 Free is auto-injected if not already on the page.
