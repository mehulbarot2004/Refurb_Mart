# Generated by Django 5.1.1 on 2025-03-20 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_refurbishedproductmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='refurbishedproductmodel',
            name='userid',
        ),
    ]
