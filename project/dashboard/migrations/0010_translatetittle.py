# Generated by Django 5.0.2 on 2024-04-12 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_services_language'),
        ('post', '0004_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='TranslateTittle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(max_length=4000, verbose_name='content')),
                ('active', models.BooleanField(choices=[(True, 'Active'), (False, 'Inactive')], default=True, verbose_name='active')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='services_lan', to='post.language', verbose_name='language')),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services_lang', to='dashboard.services', verbose_name='services')),
            ],
        ),
    ]