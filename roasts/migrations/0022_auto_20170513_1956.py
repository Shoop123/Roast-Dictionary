# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-13 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roasts', '0021_auto_20170502_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.TextField(),
        ),
    ]