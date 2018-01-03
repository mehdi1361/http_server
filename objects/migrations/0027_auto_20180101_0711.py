# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-01 07:11
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0026_auto_20171231_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhero',
            name='level',
            field=models.PositiveIntegerField(default=1, verbose_name='level'),
        ),
        migrations.AddField(
            model_name='userhero',
            name='next_upgrade_card_count',
            field=models.PositiveIntegerField(default=0, verbose_name='next upgrade card count'),
        ),
        migrations.AddField(
            model_name='userhero',
            name='next_upgrade_coin_cost',
            field=models.PositiveIntegerField(default=0, verbose_name='next Upgrade Coin Cost'),
        ),
        migrations.AddField(
            model_name='userhero',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='quantity card'),
        ),
        migrations.AlterField(
            model_name='hero',
            name='unique_id',
            field=models.UUIDField(default=uuid.UUID('25ec3940-f084-464a-bad6-8e04ffb5750e'), editable=False, verbose_name='unique id'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unique_id',
            field=models.UUIDField(default=uuid.UUID('25ec3940-f084-464a-bad6-8e04ffb5750e'), editable=False, verbose_name='unique id'),
        ),
    ]