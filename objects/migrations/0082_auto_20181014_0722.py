# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-14 07:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0081_auto_20180930_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalunit',
            name='unlock_league',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='objects.League'),
        ),
        migrations.AddField(
            model_name='unit',
            name='unlock_league',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='units', to='objects.League', verbose_name='unlock league'),
        ),
    ]
