# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 08:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0070_auto_20180117_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalusercard',
            name='next_upgrade_card_count',
        ),
        migrations.RemoveField(
            model_name='historicalusercard',
            name='next_upgrade_coin_cost',
        ),
        migrations.RemoveField(
            model_name='historicaluserhero',
            name='next_upgrade_card_count',
        ),
        migrations.RemoveField(
            model_name='historicaluserhero',
            name='next_upgrade_coin_cost',
        ),
        migrations.RemoveField(
            model_name='historicaluseritem',
            name='next_upgrade_card_count',
        ),
        migrations.RemoveField(
            model_name='historicaluseritem',
            name='next_upgrade_coin_cost',
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='next_upgrade_card_count',
        ),
        migrations.RemoveField(
            model_name='usercard',
            name='next_upgrade_coin_cost',
        ),
        migrations.RemoveField(
            model_name='userhero',
            name='next_upgrade_card_count',
        ),
        migrations.RemoveField(
            model_name='userhero',
            name='next_upgrade_coin_cost',
        ),
        migrations.RemoveField(
            model_name='useritem',
            name='next_upgrade_card_count',
        ),
        migrations.RemoveField(
            model_name='useritem',
            name='next_upgrade_coin_cost',
        ),
    ]
