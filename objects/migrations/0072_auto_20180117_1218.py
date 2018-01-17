# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 12:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0071_auto_20180117_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalusercurrency',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical profile'},
        ),
        migrations.AlterModelOptions(
            name='usercurrency',
            options={'verbose_name': 'profile', 'verbose_name_plural': 'profile'},
        ),
        migrations.AlterModelTable(
            name='usercurrency',
            table='profiles',
        ),
    ]
