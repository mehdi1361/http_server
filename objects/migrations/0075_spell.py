# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-22 09:07
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0074_auto_20180117_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('char_spells_index', models.IntegerField(default=0, verbose_name='char spells index')),
                ('cost', models.IntegerField(default=0, verbose_name='cost')),
                ('is_instant', models.BooleanField(default=True, verbose_name='is_instant')),
                ('need_target_to_come_near', models.BooleanField(default=True, verbose_name='need target to come near')),
                ('spell_name', models.CharField(default='', max_length=100, verbose_name='spell name')),
                ('spell_type', models.CharField(choices=[('CriticalAttack', 'CriticalAttack'), ('Magic', 'Magic'), ('Secret', 'Secret'), ('Chakra', 'Chakra'), ('DamageReturn', 'DamageReturn')], default='Magic', max_length=50, verbose_name='spell type')),
                ('spell_impact', models.CharField(choices=[('None', 'None'), ('Low', 'Low'), ('High', 'High')], default='Low', max_length=20, verbose_name='damage type')),
                ('damage_type', models.CharField(choices=[('Low', 'Low'), ('High', 'High')], default='Low', max_length=20, verbose_name='spell_impact')),
                ('generated_action_point', models.IntegerField(default=0, verbose_name='generated action point')),
            ],
            options={
                'db_table': 'spells',
                'verbose_name': 'spell',
                'verbose_name_plural': 'spells',
            },
        ),
    ]
