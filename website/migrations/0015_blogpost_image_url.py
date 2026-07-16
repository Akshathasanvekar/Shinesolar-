from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_founder'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='image_url',
            field=models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above (e.g. a temporary stock photo link).'),
        ),
    ]
