# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-24 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_auto_20180210_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalusercurrency',
            name='need_comeback',
            field=models.BooleanField(default=False, verbose_name='nee comeback'),
        ),
        migrations.AddField(
            model_name='historicalusercurrency',
            name='next_session_remaining_seconds',
            field=models.PositiveIntegerField(default=0, verbose_name='next session remaining seconds'),
        ),
        migrations.AddField(
            model_name='historicalusercurrency',
            name='session_count',
            field=models.PositiveIntegerField(default=0, verbose_name='session count'),
        ),
        migrations.AddField(
            model_name='usercurrency',
            name='need_comeback',
            field=models.BooleanField(default=False, verbose_name='nee comeback'),
        ),
        migrations.AddField(
            model_name='usercurrency',
            name='next_session_remaining_seconds',
            field=models.PositiveIntegerField(default=0, verbose_name='next session remaining seconds'),
        ),
        migrations.AddField(
            model_name='usercurrency',
            name='session_count',
            field=models.PositiveIntegerField(default=0, verbose_name='session count'),
        ),
    ]
