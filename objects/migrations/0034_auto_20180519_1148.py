# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-19 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0033_auto_20180519_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=500, unique=True, verbose_name='device model'),
        ),
    ]
