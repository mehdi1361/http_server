# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-14 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0019_appconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('helmet', 'helmet'), ('weapon', 'weapon'), ('Armor', 'Armor'), ('Accessory', 'Accessory')], default='helmet', max_length=50, null=True, verbose_name='item type'),
        ),
    ]
