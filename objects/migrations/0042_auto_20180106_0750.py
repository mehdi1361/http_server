# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-06 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0041_historicalbenefitbox_historicalchest_historicalhero_historicalherounits_historicalleague_historicalu'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalusercard',
            name='cool_down',
            field=models.DateTimeField(null=True, verbose_name='cooldown'),
        ),
        migrations.AddField(
            model_name='usercard',
            name='cool_down',
            field=models.DateTimeField(null=True, verbose_name='cooldown'),
        ),
    ]
