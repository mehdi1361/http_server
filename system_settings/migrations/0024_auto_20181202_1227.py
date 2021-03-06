# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-02 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_settings', '0023_auto_20181202_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctm',
            name='is_must_have_hero',
            field=models.BooleanField(default=False, verbose_name='is must have hero'),
        ),
        migrations.AddField(
            model_name='ctm',
            name='is_must_have_spell',
            field=models.BooleanField(default=False, verbose_name='is must have spell'),
        ),
        migrations.AddField(
            model_name='ctm',
            name='is_must_have_troop',
            field=models.BooleanField(default=False, verbose_name='is must have troop'),
        ),
    ]
