# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-31 12:37
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0024_auto_20171231_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='level',
            field=models.PositiveIntegerField(default=0, verbose_name='level'),
        ),
        migrations.AddField(
            model_name='unit',
            name='level',
            field=models.PositiveIntegerField(default=0, verbose_name='level'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='unique_id',
            field=models.UUIDField(default=uuid.UUID('fb151cac-beed-4ea7-ac52-eef07a2ba463'), editable=False, verbose_name='unique id'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unique_id',
            field=models.UUIDField(default=uuid.UUID('fb151cac-beed-4ea7-ac52-eef07a2ba463'), editable=False, verbose_name='unique id'),
        ),
    ]
