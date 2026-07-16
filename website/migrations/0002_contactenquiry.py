from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('website', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='ContactEnquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True)),
                ('service', models.CharField(blank=True, max_length=100)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Contact Enquiries'},
        ),
    ]
