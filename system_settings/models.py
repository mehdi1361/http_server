# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from objects.models import League, Unit, Hero
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.db.models import signals
from  base import fields


@python_2_unicode_compatible
class CTM(Base):
    CHEST_TYPE = (
        ('W', 'wooden'),
        ('S', 'silver'),
        ('G', 'gold'),
        ('C', 'crystal'),
        ('M', 'magical'),
        ('L', 'Legendary'),
    )

    chest_type = models.CharField(_('chest type'), max_length=50, default='W', choices=CHEST_TYPE)
    league = models.ForeignKey(League, verbose_name=_('league'), related_name='ctm_chests')

    min_coin = models.PositiveIntegerField(_('min coin'), default=0)
    max_coin = models.PositiveIntegerField(_('max coin'), default=0)

    min_gem = models.PositiveIntegerField(_('min gem'), default=0)
    max_gem = models.PositiveIntegerField(_('max gem'), default=0)

    min_troop = models.PositiveIntegerField(_('min troop'), default=0)
    max_troop = models.PositiveIntegerField(_('max troop'), default=0)
    chance_troop = models.FloatField(_('chance troop'), default=0)

    min_hero = models.PositiveIntegerField(_('min hero'), default=0)
    max_hero = models.PositiveIntegerField(_('max hero'), default=0)
    chance_hero = models.FloatField(_('chance hero'), default=0)

    total = models.PositiveIntegerField(_('total'), default=0)
    card_try = models.PositiveIntegerField(_('count try'), default=0)

    class Meta:
        verbose_name = _('ctm')
        verbose_name_plural = _('ctm')
        db_table = 'ctm'
        unique_together = ('chest_type', 'league')

    def __str__(self):
        return '{}-{}'.format(self.chest_type, self.league.league_name)


@python_2_unicode_compatible
class CTMUnit(Base):
    ctm = models.ForeignKey(CTM, verbose_name=_('ctm'), related_name='units')
    unit = models.ForeignKey(Unit, verbose_name=_('unit'), related_name='ctms')
    enable = models.BooleanField(_('enable'), default=True)

    class Meta:
        verbose_name = _('ctm_unit')
        verbose_name_plural = _('ctm_units')
        db_table = 'ctm_units'
        unique_together = ('ctm', 'unit')

    def __str__(self):
        return 'ctm-{}-{}'.format(self.ctm.id, self.unit.moniker)


@python_2_unicode_compatible
class CTMHero(Base):
    ctm = models.ForeignKey(CTM, verbose_name=_('ctm'), related_name='heroes')
    hero = models.ForeignKey(Hero, verbose_name=_('unit'), related_name='ctms')
    enable = models.BooleanField(_('enable'), default=True)

    class Meta:
        verbose_name = _('ctm_hero')
        verbose_name_plural = _('ctm_heroes')
        db_table = 'ctm_heroes'
        unique_together = ('ctm', 'hero')

    def __str__(self):
        return 'ctm-{}-{}'.format(self.ctm.id, self.hero.moniker)


@python_2_unicode_compatible
class BotMatchMaking(Base):
    bot_ai = fields.IntegerRangeField(verbose_name=_('bot ai'), default=0, min_value=0, max_value=100)
    strike_number = models.IntegerField(_('strike number'), unique=True)
    min_level = models.IntegerField(_('min level'), default=0)
    max_level = models.IntegerField(_('max level'), default=0)
    step_forward = models.IntegerField(_('step forward'), default=0)
    step_backward = models.IntegerField(_('step backward'), default=0)

    class Meta:
        verbose_name = _('bot_match_making')
        verbose_name_plural = _('bot_match_makings')
        db_table = 'bot_match_makings'

    def __str__(self):
        return 'match_making-{}-{}'.format(self.bot_ai, self.strike_number)


def assigned_item_to_ctm(sender, instance, created, **kwargs):
    if created:
        for unit in Unit.objects.all():
            CTMUnit.objects.create(unit=unit, ctm=instance)

        for hero in Hero.objects.all():
            CTMHero.objects.create(hero=hero, ctm=instance)


signals.post_save.connect(assigned_item_to_ctm, sender=CTM)
