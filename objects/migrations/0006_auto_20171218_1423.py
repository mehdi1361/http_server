# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 14:23
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objects', '0005_auto_20171218_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('gem_quantity', models.PositiveIntegerField(default=None, verbose_name='gem quantity')),
                ('coin_quantity', models.PositiveIntegerField(default=None, verbose_name='coin quantity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_chest', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_chest',
                'verbose_name': 'user_chest',
                'verbose_name_plural': 'user_chest',
            },
        ),
        migrations.RenameModel(
            old_name='UserBy',
            new_name='UserBuy',
        ),
        migrations.AlterModelOptions(
            name='userbuy',
            options={'verbose_name': 'user_buy', 'verbose_name_plural': 'user_buy'},
        ),
        migrations.AlterModelTable(
            name='userbuy',
            table='user_buy',
        ),
    ]
