# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-07 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0060_auto_20180707_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='demoting_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='demoting count'),
        ),
        migrations.AlterField(
            model_name='league',
            name='min_trophy',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='min trophy'),
        ),
        migrations.AlterField(
            model_name='league',
            name='play_off_start_gem',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='play off start gem '),
        ),
        migrations.AlterField(
            model_name='league',
            name='play_off_start_gem_1',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='play off start gem 1'),
        ),
        migrations.AlterField(
            model_name='league',
            name='play_off_start_gem_2',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='play off start gem 2'),
        ),
        migrations.AlterField(
            model_name='league',
            name='play_off_unlock_score',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='play off unlock score'),
        ),
        migrations.AlterField(
            model_name='league',
            name='playoff_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='playoff count'),
        ),
        migrations.AlterField(
            model_name='league',
            name='playoff_range',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='playoff range'),
        ),
        migrations.AlterField(
            model_name='league',
            name='promoting_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='promoting count'),
        ),
        migrations.AlterField(
            model_name='league',
            name='win_promoting_count',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='win promoting count'),
        ),
    ]
