# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-18 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctm',
            name='chance_hero',
            field=models.PositiveIntegerField(default=0, verbose_name='chance hero'),
        ),
        migrations.AddField(
            model_name='ctm',
            name='chance_troop',
            field=models.PositiveIntegerField(default=0, verbose_name='chance troop'),
        ),
    ]
