# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-26 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0051_auto_20180626_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leagueuser',
            name='win_count',
        ),
        migrations.AddField(
            model_name='leagueuser',
            name='lose_count',
            field=models.PositiveIntegerField(default=0, verbose_name='lose count'),
        ),
    ]
