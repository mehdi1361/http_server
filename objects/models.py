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
    image_logo = models.ImageField(_('image'), upload_to='unit/logo')
    image = models.ImageField(_('image'), upload_to='unit/image')
    user = models.ManyToManyField(User, through='UserUnits', related_name='units')

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')
        db_table = 'unit'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Hero(BaseUnit, Base):
    name = models.CharField(_('name'), max_length=50, unique=True)
    image_logo = models.ImageField(_('image'), upload_to='hero/logo')
    image = models.ImageField(_('image'), upload_to='hero/image')

    class Meta:
        verbose_name = _('hero')
        verbose_name_plural = _('heroes')
        db_table = 'hero'

    def __str__(self):
        return '{}'.format(self.name)


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