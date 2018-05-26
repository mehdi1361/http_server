# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-12 13:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0015_auto_20180512_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencylog',
            name='type_buy',
            field=models.CharField(choices=[('GEM', 'gem'), ('COIN', 'coin'), ('CARD', 'card'), ('CHEST', 'chest'), ('UPDATE_UNIT', 'update_unit'), ('UPDATE_HERO', 'update_hero')], max_length=10, verbose_name='buy type'),
        ),
    ]