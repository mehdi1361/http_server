# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 07:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0067_auto_20180116_1249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='level',
        ),
        migrations.RemoveField(
            model_name='historicalhero',
            name='level',
        ),
        migrations.RemoveField(
            model_name='historicalunit',
            name='level',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='level',
        ),
    ]
