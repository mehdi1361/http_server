# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-19 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0032_auto_20180519_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='objects.UserCurrency', verbose_name='user'),
        ),
    ]