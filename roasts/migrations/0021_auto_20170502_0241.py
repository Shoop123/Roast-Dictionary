# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-02 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roasts', '0020_auto_20170502_0211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]