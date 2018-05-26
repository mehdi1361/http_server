# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-16 06:57
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BattleTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('state', models.CharField(choices=[('start', 'start'), ('turn_change', 'turn_change'), ('action', 'action'), ('end', 'end')], default='start', max_length=50, verbose_name='state')),
                ('battle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='reports.Battle', verbose_name='battle')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]