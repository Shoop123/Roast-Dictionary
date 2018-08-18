# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 08:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('roasts', '0002_keys_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='keys',
            options={'get_latest_by': 'created_at'},
        ),
        migrations.AlterField(
            model_name='keys',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
