# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-20 06:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_battle_battle_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='battle_id',
            field=models.CharField(default=None, max_length=200, null=True, unique=True, verbose_name='battle id'),
        ),
    ]
