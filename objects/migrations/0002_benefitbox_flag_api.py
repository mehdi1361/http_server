# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 15:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefitbox',
            name='flag_api',
            field=models.BooleanField(default=False, verbose_name='show box for user'),
        ),
    ]