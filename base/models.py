# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db import models
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


