# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-29 13:31
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0006_auto_20180306_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='special_offer',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, null=True, verbose_name='special offer'),
        ),
    ]