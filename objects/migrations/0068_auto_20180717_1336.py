# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0067_auto_20180714_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalusercurrency',
            name='lose_count',
            field=models.PositiveIntegerField(default=0, verbose_name='lose count'),
        ),
        migrations.AddField(
            model_name='historicalusercurrency',
            name='win_count',
            field=models.PositiveIntegerField(default=0, verbose_name='win count'),
        ),
        migrations.AddField(
            model_name='usercurrency',
            name='lose_count',
            field=models.PositiveIntegerField(default=0, verbose_name='lose count'),
        ),
        migrations.AddField(
            model_name='usercurrency',
            name='win_count',
            field=models.PositiveIntegerField(default=0, verbose_name='win count'),
        ),
    ]
