# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-02 02:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roasts', '0019_alert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='visible',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]