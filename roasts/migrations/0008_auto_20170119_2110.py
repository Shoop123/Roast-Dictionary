# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-01-19 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roasts', '0007_auto_20170117_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]