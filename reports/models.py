# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from base.models import Base
from objects.models import UserHero, Unit


@python_2_unicode_compatible
class Battle(Base):
    STATUS = (
        ('start', 'start'),
        ('end', 'end'),
    )
    player_1 = models.CharField(_("player 1"), max_length=1000)
    player_1_bot = models.BooleanField(_('player 1 is bot'), default=False)
    player_2 = models.CharField(_("player 1"), max_length=1000)
    player_2_bot = models.BooleanField(_('player 2 is bot'), default=False)

    status = models.CharField(_('status'), max_length=5, choices=STATUS, default='start')
    battle_id = models.CharField(_('battle id'), max_length=200, unique=True, default=None, null=True)

    class Meta:
        verbose_name = _('battle')
        verbose_name_plural = _('battles')
        db_table = 'battles'

    def __str__(self):
        return '{}'.format(self.id)


class BattleTransaction(Base):
    STATE = (
        ('start', 'start'),
        ('turn_change', 'turn_change'),
        ('action', 'action'),
        ('end', 'end'),
    )
    battle = models.ForeignKey(Battle, verbose_name=_('battle'), related_name='transactions')
    state = models.CharField(_('state'), max_length=50, choices=STATE, default='start')

    class Meta:
        verbose_name = _('battle transaction')
        verbose_name_plural = _('battle transactions')
        db_table = 'battle_transaction'

    def __str__(self):
        return '{}'.format(self.id)


class UserHeroSummary(UserHero):
    class Meta:
        proxy = True
        verbose_name = 'UserHero Summary'
        verbose_name_plural = 'UserHeroes Summary'


@python_2_unicode_compatible
class TroopReport(Base):
    troop = models.ForeignKey(Unit, verbose_name=_('troop'), related_name='fight_reports')
    win = models.PositiveIntegerField(_('win count'), default=0)
    lose = models.PositiveIntegerField(_('lose count'), default=0)

    class Meta:
        verbose_name = _('troop_report')
        verbose_name_plural = _('troop_reports')
        db_table = 'troop_reports'

    def __str__(self):
        return '{}-win:{} - lose:{}'.format(self.troop.moniker, self.win, self.lose)

