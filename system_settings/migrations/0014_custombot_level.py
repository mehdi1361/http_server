# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 13:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0013_auto_20181015_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='custombot',
            name='level',
            field=models.PositiveIntegerField(default=1, verbose_name='level'),
        ),
    ]