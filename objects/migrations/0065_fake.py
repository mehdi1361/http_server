# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-11 13:53
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0064_auto_20180710_0656'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='fake description')),
                ('enable', models.BooleanField(default=True, verbose_name='enable')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fakes', to='objects.League', verbose_name='league')),
            ],
            options={
                'db_table': 'fakes',
                'verbose_name': 'fake',
                'verbose_name_plural': 'fakes',
            },
        ),
    ]