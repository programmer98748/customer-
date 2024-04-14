# Generated by Django 5.0.2 on 2024-04-12 23:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_delete_post'),
        ('post', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='services', to='post.language', verbose_name='language'),
        ),
    ]