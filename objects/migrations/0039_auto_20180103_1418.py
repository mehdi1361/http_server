# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-03 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import objects.validators


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0038_auto_20180103_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchest',
            name='sequence_number',
            field=models.PositiveIntegerField(default=0, validators=[objects.validators.validate_sequence], verbose_name='sequence number'),
        ),
    ]