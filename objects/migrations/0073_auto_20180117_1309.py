# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-17 13:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0072_auto_20180117_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercurrency',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_currency', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
