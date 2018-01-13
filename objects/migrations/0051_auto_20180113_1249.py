# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-13 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0050_auto_20180113_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluserchest',
            name='status',
            field=models.CharField(choices=[('close', 'close'), ('opening', 'opening'), ('ready', 'ready'), ('used', 'used')], default='close', max_length=50, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='userchest',
            name='status',
            field=models.CharField(choices=[('close', 'close'), ('opening', 'opening'), ('ready', 'ready'), ('used', 'used')], default='close', max_length=50, verbose_name='status'),
        ),
    ]