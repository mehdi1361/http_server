# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db import models


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
    name = models.CharField(_('name'), max_length=50)
    health = models.IntegerField(_('health'), default=100)
    shield = models.IntegerField(_('shield'), default=0)
    attack = models.IntegerField(_('attack'), default=10)
    critical_chance = models.FloatField(_('critical chance'), default=0.01)
    critical_ratio = models.FloatField(_('critical ratio'), default=0.01)
    miss_chance = models.FloatField(_('miss chance'), default=0.00)
    dodge_chance = models.FloatField(_('dodge chance'), default=0.00)
    dexterity = models.CharField(_('dexterity'), max_length=50,  default='MIDDLE', choices=DEXTERITY)

    class Meta:
        abstract = True
