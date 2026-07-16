from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_blogpost_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro_image', models.ImageField(blank=True, help_text='Photo shown next to "Who We Are" at the top of the About page. Uploading here always overrides the link below.', null=True, upload_to='about/')),
                ('intro_image_url', models.URLField(blank=True, default='', help_text='Optional: used only if no photo is uploaded above.')),
                ('gallery_image_1', models.ImageField(blank=True, help_text='1st photo in the Projects Gallery strip.', null=True, upload_to='about/')),
                ('gallery_image_1_url', models.URLField(blank=True, default='')),
                ('gallery_image_2', models.ImageField(blank=True, help_text='2nd photo in the Projects Gallery strip.', null=True, upload_to='about/')),
                ('gallery_image_2_url', models.URLField(blank=True, default='')),
                ('gallery_image_3', models.ImageField(blank=True, help_text='3rd photo in the Projects Gallery strip.', null=True, upload_to='about/')),
                ('gallery_image_3_url', models.URLField(blank=True, default='')),
            ],
            options={
                'verbose_name_plural': 'About Page',
            },
        ),
    ]
