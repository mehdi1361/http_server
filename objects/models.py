# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, BaseUnit
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


# Create your models here.

@python_2_unicode_compatible
class BenefitBox(Base):
    TYPE = (
        ('GEM', 'gem'),
        ('COIN', 'coin')
    )
    name = models.CharField(_('name'), max_length=40)
    box = models.CharField(_('box'), max_length=4, choices=TYPE)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    flag_api = models.BooleanField(_('show box for user'), default=False)
    user = models.ManyToManyField(User, through='UserBuy', related_name='benefits')

    class Meta:
        verbose_name = _('benefit_box')
        verbose_name_plural = _('benefit_boxes')
        db_table = 'benefit_box'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Unit(BaseUnit, Base):
    user = models.ManyToManyField(User, through='UserUnits', related_name='units')

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')
        db_table = 'unit'

    def __str__(self):
        return '{}'.format(self.moniker)


@python_2_unicode_compatible
class Hero(BaseUnit, Base):
    chakra_health = models.IntegerField(_('chakra health'), default=100)
    chakra_shield = models.IntegerField(_('chakra shield'), default=0)
    chakra_attack = models.IntegerField(_('chakra attack'), default=10)
    chakra_critical_chance = models.FloatField(_('chakra critical chance'), default=0.01)
    chakra_critical_ratio = models.FloatField(_('chakra critical ratio'), default=0.01)
    chakra_miss_chance = models.FloatField(_('chakra miss chance'), default=0.00)
    chakra_dodge_chance = models.FloatField(_('chakra dodge chance'), default=0.00)
    unit_list = models.ManyToManyField(Unit, through='HeroUnits', related_name='hero_unit')

    class Meta:
        verbose_name = _('hero')
        verbose_name_plural = _('heroes')
        db_table = 'hero'

    def __str__(self):
        return '{}'.format(self.moniker)


class UserBuy(Base):
    user = models.ForeignKey(User, related_name='user_buy')
    benefit = models.ForeignKey(BenefitBox, related_name='user_buy')

    class Meta:
        verbose_name = _('user_buy')
        verbose_name_plural = _('user_buy')
        db_table = 'user_buy'


@python_2_unicode_compatible
class UserChest(Base):
    user = models.ForeignKey(User, related_name='user_chest')
    gem = models.PositiveIntegerField(_('gem quantity'), default=0)
    coin = models.PositiveIntegerField(_('coin quantity'), default=0)

    class Meta:
        verbose_name = _('user_chest')
        verbose_name_plural = _('user_chest')
        db_table = 'user_chest'

    def __str__(self):
        return '{}, gem:{}, coin:{}'.format(self.user, self.gem, self.coin)


@python_2_unicode_compatible
class UserUnits(Base):
    user = models.ForeignKey(User, related_name='user_units')
    unit = models.ForeignKey(Unit, related_name='user_units')
    next_upgrade_coin_cost = models.PositiveIntegerField(_('next Upgrade Coin Cost'), default=0)
    next_upgrade_card_count = models.PositiveIntegerField(_('next upgrade card count'), default=0)
    level = models.PositiveIntegerField(_('level'), default=1)
    cur_card_count = models.PositiveIntegerField(_('cur card count'), default=1)

    class Meta:
        verbose_name = _('user_unit')
        verbose_name_plural = _('user_unit')
        db_table = 'user_unit'
        unique_together = ('user', 'unit')

    def __str__(self):
        return 'user:{}, unit:{}'.format(self.user.username, self.unit.name)


@python_2_unicode_compatible
class HeroUnits(Base):
    hero = models.ForeignKey(Hero, related_name='units_hero')
    unit = models.ForeignKey(Unit, related_name='unit_heroes')
    enable_hero = models.BooleanField(_('enable hero'), default=False)

    class Meta:
        verbose_name = _('hero_unit')
        verbose_name_plural = _('hero_units')
        db_table = 'hero_units'
        unique_together = ('hero', 'unit')

    def __str__(self):
        return 'hero:{}, unit:{}'.format(self.hero.moniker, self.unit.moniker)
