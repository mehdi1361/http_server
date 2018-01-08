# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-08 09:15
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_shop_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='special_offer',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None, null=True, verbose_name='chests'),
        ),
    ]
