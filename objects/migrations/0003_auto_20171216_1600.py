# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-16 16:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0002_benefitbox_flag_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
    ]