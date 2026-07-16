from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_contactenquiry'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('slug', models.SlugField(max_length=320, unique=True)),
                ('excerpt', models.TextField(blank=True, max_length=400)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Blog Posts',
                'ordering': ['-created_at'],
            },
        ),
    ]
