from django.db import migrations


DEFAULT_SOLUTIONS = [
    {
        "title": "Residential Solar",
        "description": "Rooftop solar for homes with subsidy support. Cut your electricity bill by 80%.",
        "icon_class": "fa-solid fa-house",
        "image_url": "https://images.unsplash.com/photo-1655300256335-beef51a914fe?fm=jpg&q=80&w=800&auto=format&fit=crop",
        "order": 1,
    },
    {
        "title": "Commercial Solar",
        "description": "Large-scale solar for offices, shops and commercial complexes.",
        "icon_class": "fa-solid fa-building",
        "image_url": "https://images.unsplash.com/photo-1707247111552-aaf74241058b?fm=jpg&q=80&w=800&auto=format&fit=crop",
        "order": 2,
    },
    {
        "title": "Industrial Solar",
        "description": "High-capacity solar plants for factories and industrial units.",
        "icon_class": "fa-solid fa-industry",
        "image_url": "https://images.unsplash.com/photo-1509391366360-2e959784a276?fm=jpg&q=80&w=800&auto=format&fit=crop",
        "order": 3,
    },
    {
        "title": "Solar Maintenance",
        "description": "Annual maintenance contracts to keep your system running at peak performance.",
        "icon_class": "fa-solid fa-screwdriver-wrench",
        "image_url": "https://images.unsplash.com/photo-1668097613572-40b7c11c8727?fm=jpg&q=80&w=800&auto=format&fit=crop",
        "order": 4,
    },
    {
        "title": "Battery Backup",
        "description": "Reliable energy storage solutions for uninterrupted power.",
        "icon_class": "fa-solid fa-battery-full",
        "image": "solutions/battery-backup-default.png",
        "order": 5,
    },
    {
        "title": "EV Charging",
        "description": "Charge electric vehicles using clean solar energy.",
        "icon_class": "fa-solid fa-charging-station",
        "image": "solutions/ev-charging-default.png",
        "order": 6,
    },
]


def seed_solutions(apps, schema_editor):
    SolarSolution = apps.get_model('website', 'SolarSolution')
    # Only seed on a fresh install — never overwrite an existing dashboard setup
    if SolarSolution.objects.exists():
        return
    for data in DEFAULT_SOLUTIONS:
        SolarSolution.objects.create(is_active=True, **data)


def remove_solutions(apps, schema_editor):
    SolarSolution = apps.get_model('website', 'SolarSolution')
    SolarSolution.objects.filter(
        title__in=[d["title"] for d in DEFAULT_SOLUTIONS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_solarsolution_image_url_alter_solarsolution_image'),
    ]

    operations = [
        migrations.RunPython(seed_solutions, remove_solutions),
    ]
