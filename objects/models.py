# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, BaseUnit
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models import signals
from .validators import validate_percent, validate_sequence
from django.conf import settings
from django.contrib.postgres.fields import JSONField


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
    user = models.ManyToManyField(User, through='UserCard', related_name='units')
    heroes = models.ManyToManyField('Hero', through='HeroUnits', related_name='hero')

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
    units = models.ManyToManyField(Unit, through='HeroUnits', related_name='hero')
    user = models.ManyToManyField(User, through='UserHero', related_name='hero')

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
class UserCurrency(Base):
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
class HeroUnits(Base):
    hero = models.ForeignKey(Hero, related_name='units_hero')
    unit = models.ForeignKey(Unit, related_name='unit_heroes')

    class Meta:
        verbose_name = _('hero_unit')
        verbose_name_plural = _('hero_units')
        db_table = 'hero_units'
        unique_together = ('hero', 'unit')

    def __str__(self):
        return 'hero:{}, unit:{}'.format(self.hero.moniker, self.unit.moniker)


@python_2_unicode_compatible
class UserHero(Base):
    user = models.ForeignKey(User, related_name='user_hero')
    hero = models.ForeignKey(Hero, related_name='user_hero')
    enable_hero = models.BooleanField(_('enable hero'), default=False)
    quantity = models.PositiveIntegerField(_('quantity card'), default=0)
    next_upgrade_coin_cost = models.PositiveIntegerField(_('next Upgrade Coin Cost'), default=0)
    next_upgrade_card_count = models.PositiveIntegerField(_('next upgrade card count'), default=0)
    level = models.PositiveIntegerField(_('level'), default=1)

    class Meta:
        verbose_name = _('user_hero')
        verbose_name_plural = _('user_hero')
        db_table = 'user_hero'
        unique_together = ('user', 'hero')

    def __str__(self):
        return 'user:{}, hero:{}'.format(self.user.username, self.hero.moniker)


@python_2_unicode_compatible
class UserCard(Base):
    user = models.ForeignKey(User, verbose_name=_('username'), related_name='cards')
    character = models.ForeignKey(Unit, verbose_name=_('character'), related_name='cards')
    quantity = models.PositiveIntegerField(_('quantity card'), default=0)
    next_upgrade_coin_cost = models.PositiveIntegerField(_('next Upgrade Coin Cost'), default=0)
    next_upgrade_card_count = models.PositiveIntegerField(_('next upgrade card count'), default=0)
    level = models.PositiveIntegerField(_('level'), default=1)

    class Meta:
        verbose_name = _('user_card')
        verbose_name_plural = _('user_cards')
        db_table = 'user_card'
        unique_together = ('user', 'character')

    def __str__(self):
        return '{}'.format(self.quantity)


@python_2_unicode_compatible
class League(Base):
    name = models.CharField(_('name'), max_length=150)
    min_score = models.PositiveIntegerField(_('score for enter the league'), default=0)
    description = models.TextField(_('description'), null=True, default='')

    class Meta:
        verbose_name = _('league')
        verbose_name_plural = _('leagues')
        db_table = 'leagues'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Chest(Base):
    CHEST_TYPE = (
        ('W', 'wooden'),
        ('S', 'silver'),
        ('G', 'gold'),
        ('C', 'crystal'),
    )

    chest_type = models.CharField(_('chest type'), max_length=50, default='w', choices=CHEST_TYPE)
    league = models.ForeignKey(League, verbose_name=_('chest'), related_name='chests')
    min_coin = models.PositiveIntegerField(_('min coin'), default=0)
    max_coin = models.PositiveIntegerField(_('max coin'), default=0)
    min_gem = models.PositiveIntegerField(_('min gem'), default=0)
    max_gem = models.PositiveIntegerField(_('max gem'), default=0)
    new_card_chance = models.PositiveIntegerField(_('new card chance percentage'), default=1,
                                                  validators=[validate_percent])
    hero_card = models.PositiveIntegerField(_('hero card count'), default=0)
    unit_card = models.PositiveIntegerField(_('unit card count'), default=3)

    class Meta:
        verbose_name = _('chest')
        verbose_name_plural = _('chest')
        db_table = 'chest'
        unique_together = ('league', 'chest_type')

    def __str__(self):
        return '{}'.format(self.chest_type)


class UserChest(Base):
    TYPE = (
        ('free', 'FREE'),
        ('non-free', 'NON-FREE')
    )
    STATUS = (
        ('close', 'close'),
        ('opening', 'opening'),
        ('ready', 'ready')
    )

    user = models.ForeignKey(User, verbose_name=_('user'), related_name='chests')
    chest = models.ForeignKey(Chest, verbose_name=_('chest'), related_name='users')
    chest_type = models.CharField(_('chest type'), max_length=50, choices=TYPE, default='free')
    status = models.CharField(_('status'), max_length=50, choices=STATUS, default='close')
    sequence_number = models.PositiveIntegerField(_('sequence number'), default=0, validators=[validate_sequence])
    cards = JSONField(verbose_name=_('cards'), default=None, null=True)

    @classmethod
    def deck_is_open(cls, user, chest_type):
        if cls.objects.filter(user=user, chest_type=chest_type).count() >= settings.DECK_COUNT[chest_type]:
            return False

        return True

    @classmethod
    def get_sequence(cls, user):
        last_chest = cls.objects.filter(user=user).last()
        return 0 if last_chest is None else last_chest.sequence_number, \
               settings.CHEST_SEQUENCE[0 if last_chest is None else last_chest.sequence_number]

    class Meta:
        verbose_name = _('user_chest')
        verbose_name_plural = _('user_chest')
        db_table = 'user_chests'

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.chest.chest_type)


def create_user_cards(sender, instance, created, **kwargs):
    if created:
        for unit in Unit.objects.all():
            UserCard.objects.create(user=instance, character=unit)


signals.post_save.connect(create_user_cards, sender=User)
