# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 10:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0041_auto_20180618_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='max_trophy',
        ),
        migrations.AddField(
            model_name='leagueuser',
            name='rank',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='rank'),
        ),
    ]
