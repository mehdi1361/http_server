# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from objects.models import League
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class CTM(Base):
    CHEST_TYPE = (
        ('W', 'wooden'),
        ('S', 'silver'),
        ('G', 'gold'),
        ('C', 'crystal'),
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