# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-10 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0045_auto_20180110_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserchest',
            name='chest_type',
            field=models.CharField(choices=[('free', 'FREE'), ('non_free', 'NON_FREE')], default='free', max_length=50, verbose_name='chest type'),
        ),
        migrations.AlterField(
            model_name='userchest',
            name='chest_type',
            field=models.CharField(choices=[('free', 'FREE'), ('non_free', 'NON_FREE')], default='free', max_length=50, verbose_name='chest type'),
        ),
    ]
