# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 15:23
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('objects', '0008_auto_20171218_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_units', to='objects.Unit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_units', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_unit',
                'verbose_name': 'user_unit',
                'verbose_name_plural': 'user_unit',
            },
        ),
        migrations.AlterField(
            model_name='benefitbox',
            name='user',
            field=models.ManyToManyField(related_name='benefits', through='objects.UserBuy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='unit',
            name='user',
            field=models.ManyToManyField(related_name='units', through='objects.UserUnits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='userunits',
            unique_together=set([('user', 'unit')]),
        ),
    ]