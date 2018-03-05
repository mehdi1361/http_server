# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-28 10:47
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0008_auto_20180227_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSpell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('char_spells_index', models.IntegerField(default=0, verbose_name='char spells index')),
                ('cost', models.IntegerField(default=0, verbose_name='cost')),
                ('spell_name', models.CharField(default='', max_length=100, verbose_name='spell name')),
                ('spell_type', models.CharField(choices=[('Magic', 'Magic'), ('Secret', 'Secret'), ('Chakra', 'Chakra'), ('DamageReturn', 'DamageReturn')], default='Magic', max_length=50, verbose_name='spell type')),
                ('generated_action_point', models.IntegerField(default=0, verbose_name='generated action point')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='duration turn')),
                ('need_action_point', models.PositiveIntegerField(default=0, verbose_name='need action point')),
                ('cool_down_duration', models.PositiveIntegerField(default=0, verbose_name='cool down duration')),
                ('hero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='objects.Hero', verbose_name='hero')),
            ],
            options={
                'db_table': 'hero_spells',
                'verbose_name': 'hero_spell',
                'verbose_name_plural': 'hero_spells',
            },
        ),
        migrations.CreateModel(
            name='UnitSpell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='created date')),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='params')),
                ('char_spells_index', models.IntegerField(default=0, verbose_name='char spells index')),
                ('cost', models.IntegerField(default=0, verbose_name='cost')),
                ('spell_name', models.CharField(default='', max_length=100, verbose_name='spell name')),
                ('spell_type', models.CharField(choices=[('Magic', 'Magic'), ('Secret', 'Secret'), ('Chakra', 'Chakra'), ('DamageReturn', 'DamageReturn')], default='Magic', max_length=50, verbose_name='spell type')),
                ('generated_action_point', models.IntegerField(default=0, verbose_name='generated action point')),
                ('duration', models.PositiveIntegerField(default=0, verbose_name='duration turn')),
                ('need_action_point', models.PositiveIntegerField(default=0, verbose_name='need action point')),
                ('cool_down_duration', models.PositiveIntegerField(default=0, verbose_name='cool down duration')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spells', to='objects.Unit', verbose_name='unit')),
            ],
            options={
                'db_table': 'unit_spells',
                'verbose_name': 'unit_spell',
                'verbose_name_plural': 'unit_spells',
            },
        ),
        migrations.RemoveField(
            model_name='spelleffect',
            name='spell',
        ),
        migrations.DeleteModel(
            name='Spell',
        ),
        migrations.DeleteModel(
            name='SpellEffect',
        ),
    ]