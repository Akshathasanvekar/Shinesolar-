from django.db import migrations


DEFAULT_SLIDES = [
    {
        "title": "Industrial Solar Installation",
        "image_url": "https://images.unsplash.com/photo-1509391366360-2e959784a276?fm=jpg&q=80&w=1600&auto=format&fit=crop",
        "order": 1,
    },
    {
        "title": "Rooftop Solar Panels",
        "image_url": "https://images.unsplash.com/photo-1613665813446-82a78c468a1d?fm=jpg&q=80&w=1600&auto=format&fit=crop",
        "order": 2,
    },
    {
        "title": "Residential Solar Energy",
        "image_url": "https://images.unsplash.com/photo-1655300256335-beef51a914fe?fm=jpg&q=80&w=1600&auto=format&fit=crop",
        "order": 3,
    },
]


def seed_slides(apps, schema_editor):
    HeroSlide = apps.get_model('website', 'HeroSlide')
    # Only seed on a fresh install — never overwrite an existing dashboard setup
    if HeroSlide.objects.exists():
        return
    for data in DEFAULT_SLIDES:
        HeroSlide.objects.create(is_active=True, **data)


def remove_slides(apps, schema_editor):
    HeroSlide = apps.get_model('website', 'HeroSlide')
    HeroSlide.objects.filter(
        title__in=[d["title"] for d in DEFAULT_SLIDES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_heroslide_image_url_alter_heroslide_image'),
    ]

    operations = [
        migrations.RunPython(seed_slides, remove_slides),
    ]
