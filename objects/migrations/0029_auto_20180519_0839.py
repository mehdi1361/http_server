# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-19 08:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0028_auto_20180519_0838'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([]),
        ),
    ]
