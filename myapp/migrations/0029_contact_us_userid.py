# Generated by Django 5.1.1 on 2025-04-11 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_remove_contact_us_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_us',
            name='userid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.registermodel'),
        ),
    ]
