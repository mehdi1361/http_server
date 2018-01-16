# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-15 11:28
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0052_auto_20180113_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('name', models.CharField(max_length=50, verbose_name='item_type')),
                ('damage', models.IntegerField(default=0, verbose_name='damage')),
                ('shield', models.IntegerField(default=0, verbose_name='shield')),
                ('health', models.IntegerField(default=0, verbose_name='health')),
                ('critical_ratio', models.IntegerField(default=0, verbose_name='critical ratio')),
                ('critical_chance', models.IntegerField(default=0, verbose_name='critical chance')),
                ('dodge_chance', models.IntegerField(default=0, verbose_name='dodge chance')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='objects.Hero', verbose_name='hero')),
            ],
            options={
                'db_table': 'items',
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
    ]
