# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-29 12:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0073_auto_20180728_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=500, verbose_name='device model'),
        ),
    ]
