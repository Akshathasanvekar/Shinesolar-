"""
Management command: python manage.py seed_products_brands

Copies all images from the 'products and brands' folder into MEDIA_ROOT
and populates the database with ProductCategory, Product, and Brand records.

Usage:
    python manage.py seed_products_brands
    python manage.py seed_products_brands --images-dir /path/to/products_and_brands
"""

import os
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.text import slugify

from products_brands_app.models import ProductCategory, Product, Brand


# ── Category metadata (icon class → FontAwesome 6 Free) ──────────────────────
CATEGORY_META = {
    "EV Charging Solutions":  {"icon": "fa-charging-station", "order": 9},
    "Solar Accessories":      {"icon": "fa-toolbox",          "order": 6},
    "Solar Batteries":        {"icon": "fa-battery-full",     "order": 5},
    "Solar Inverters":        {"icon": "fa-plug",             "order": 4},
    "Solar Panels":           {"icon": "fa-solar-panel",      "order": 1},
    "Solar Pumps":            {"icon": "fa-water",            "order": 7},
    "Solar Street Lights":    {"icon": "fa-lightbulb",        "order": 8},
    "Solar Systems":          {"icon": "fa-network-wired",    "order": 2},
    "Solar Water Heaters":    {"icon": "fa-temperature-high", "order": 3},
}

BRANDS_FOLDER = "Selling Brands"


class Command(BaseCommand):
    help = "Seed Products and Brands from local image folder"

    def add_arguments(self, parser):
        parser.add_argument(
            '--images-dir',
            type=str,
            default=None,
            help='Path to the "products and brands" folder. '
                 'Defaults to BASE_DIR/assets/products and brands',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing records before seeding',
        )

    def handle(self, *args, **options):
        base_dir = Path(getattr(settings, 'BASE_DIR', '.'))

        images_dir = Path(options['images_dir']) if options['images_dir'] \
            else base_dir / 'assets' / 'products and brands'

        if not images_dir.exists():
            raise CommandError(
                f"Images directory not found: {images_dir}\n"
                "Copy the 'products and brands' folder next to manage.py "
                "under assets/, or pass --images-dir."
            )

        if options['clear']:
            self.stdout.write("Clearing existing records …")
            Product.objects.all().delete()
            Brand.objects.all().delete()
            ProductCategory.objects.all().delete()

        media_products = Path(settings.MEDIA_ROOT) / 'products'
        media_brands   = Path(settings.MEDIA_ROOT) / 'brands'
        media_products.mkdir(parents=True, exist_ok=True)
        media_brands.mkdir(parents=True, exist_ok=True)

        # ── Brands ────────────────────────────────────────────────────────────
        brands_src = images_dir / BRANDS_FOLDER
        if brands_src.exists():
            self.stdout.write(self.style.MIGRATE_HEADING("Seeding brands …"))
            for idx, img_path in enumerate(sorted(brands_src.glob('*.png')), 1):
                brand_name = img_path.stem          # filename without extension
                slug = slugify(brand_name)
                dest = media_brands / img_path.name
                shutil.copy2(img_path, dest)

                brand, created = Brand.objects.update_or_create(
                    slug=slug,
                    defaults={
                        'name': brand_name,
                        'logo': f'brands/{img_path.name}',
                        'order': idx,
                        'is_active': True,
                    }
                )
                status = "Created" if created else "Updated"
                self.stdout.write(f"  {status}: {brand}")
        else:
            self.stdout.write(self.style.WARNING(
                f"Brands folder not found: {brands_src}"
            ))

        # ── Product Categories & Products ─────────────────────────────────────
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding product categories …"))
        for cat_name, meta in CATEGORY_META.items():
            cat_dir = images_dir / cat_name
            if not cat_dir.exists():
                self.stdout.write(self.style.WARNING(f"  Skipping missing folder: {cat_name}"))
                continue

            cat_slug = slugify(cat_name)
            category, _ = ProductCategory.objects.update_or_create(
                slug=cat_slug,
                defaults={
                    'name': cat_name,
                    'icon': meta['icon'],
                    'order': meta['order'],
                }
            )
            self.stdout.write(f"  Category: {category}")

            for p_idx, img_path in enumerate(sorted(cat_dir.glob('*.png')), 1):
                product_name = img_path.stem
                product_slug = slugify(product_name)
                dest = media_products / img_path.name
                shutil.copy2(img_path, dest)

                product, created = Product.objects.update_or_create(
                    category=category,
                    slug=product_slug,
                    defaults={
                        'name': product_name,
                        'image': f'products/{img_path.name}',
                        'order': p_idx,
                        'is_active': True,
                    }
                )
                status = "  ✓ Created" if created else "  ↻ Updated"
                self.stdout.write(f"    {status}: {product.name}")

        self.stdout.write(self.style.SUCCESS("\n✅ Done! Products and Brands seeded successfully."))
