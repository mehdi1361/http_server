# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-04 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0014_auto_20180304_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='default',
            field=models.BooleanField(default=False, verbose_name='default'),
        ),
    ]