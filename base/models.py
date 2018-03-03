# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db import models
from multiselectfield.db.fields import MultiSelectField
from simple_history.models import HistoricalRecords
import uuid


# Create your models here.

class Base(models.Model):
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)
    updated_date = models.DateTimeField(_('created date'), auto_now=True)
    params = JSONField(_('params'), null=True, blank=True)

    class Meta:

        abstract = True


class BaseUnit(models.Model):
    DEXTERITY = (
        ('MIDDLE', 'middle'),
        ('LATE', 'late'),
        ('EARLY', 'early')
    )
    ATTACK_TYPE = (
        ('NORMAL', 'normal'),
        ('SKILLSHOT', 'skillshot'),
        ('AUTOMATIC', 'automatic')
    )
    enable_in_start = models.BooleanField(_('enable in start'), default=False)
    unique_id = models.UUIDField(_('unique id'), default=uuid.uuid4, editable=False)
    moniker = models.CharField(_('moniker'), max_length=50, unique=True, default='moniker')
    dexterity = models.CharField(_('dexterity'), max_length=50,  default='MIDDLE', choices=DEXTERITY)
    attack_type = models.CharField(_('attack type'), max_length=50, choices=ATTACK_TYPE, default='normal')

    health = models.IntegerField(_('health'), default=100)
    shield = models.IntegerField(_('shield'), default=0)
    attack = models.IntegerField(_('attack'), default=10)
    critical_chance = models.FloatField(_('critical chance'), default=0.01)
    critical_ratio = models.FloatField(_('critical ratio'), default=0.01)
    miss_chance = models.FloatField(_('miss chance'), default=0.00)
    dodge_chance = models.FloatField(_('dodge chance'), default=0.00)
    max_health = models.IntegerField(_('max health'), default=100)
    max_shield = models.IntegerField(_('max shield'), default=0)
    # level = models.PositiveIntegerField(_('level'), default=0)

    class Meta:
        abstract = True


class Spell(models.Model):
    SPELL_TYPE = (
        ('Magic', 'Magic'),
        ('Secret', 'Secret'),
    )

    char_spells_index = models.IntegerField(_('char spells index'), default=0)
    spell_name = models.CharField(_('spell name'), max_length=100, default='')
    spell_type = models.CharField(_('spell type'), max_length=50, choices=SPELL_TYPE, default='Magic')
    generated_action_point = models.IntegerField(_('generated action point'), default=0)
    need_action_point = models.PositiveIntegerField(_('need action point'), default=0)
    cool_down_duration = models.PositiveIntegerField(_('cool down duration'), default=0)

    class Meta:
        abstract = True


class SpellEffect(models.Model):
    SPELL_EFFECT_ON_CHAR = (
        ('None', 'None'),
        ('Appear', 'Appear'),
        ('NormalDamage', 'NormalDamage'),
        ('SeriousDamage', 'SeriousDamage'),
        ('Nerf', 'Nerf'),
        ('Buff', 'Buff'),
        ('Miss', 'Miss'),
        ('Dodge', 'Dodge'),
        ('Burn', 'Burn'),
        ('Fear', 'Fear'),
        ('Taunt', 'Taunt'),
        ('Revive', 'Revive'),
        ('Prepare', 'Prepare'),
        ('Protect', 'Protect'),
        ('shout', 'shout'),
    )
    is_multi_part = models.BooleanField(_('is multi part'), default=False)
    target_character_id = models.FloatField(_('target character id'), default=0)
    effect_on_character = MultiSelectField(choices=SPELL_EFFECT_ON_CHAR, null=True)
    duration = models.PositiveIntegerField(_('duration turn'), default=0)

    class Meta:
        abstract = True
