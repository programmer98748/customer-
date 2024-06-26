# Generated by Django 5.0.2 on 2024-04-12 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_services_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='Brands/')),
                ('url', models.URLField(blank=True)),
                ('create_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='services',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
