# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
import random

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from base.models import Base, BaseUnit, Spell, SpellEffect
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models import signals, Count, Sum
from .validators import validate_percent, validate_sequence
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from simple_history.models import HistoricalRecords
from django.utils import timezone
from datetime import datetime, timedelta
from django.db import transaction
# from common.utils import generate_fake_user_league


def generate_fake_user_league(league):
    fake_user_lst = []
    result = []

    fake = Fake.objects.filter(league=league).enable().first()

    for item in fake.details.all():
        for i in range(0, item.quantity):
            enable = True
            while enable:
                random_number = random.randint(0, len(settings.FAKE_USER) - 1)

                if random_number not in result:
                    result.append(random_number)
                    selected_name = settings.FAKE_USER[random_number]
                    enable = False

            fake_user_lst.append({
                "name": selected_name,
                "score": 0,
                "win_rate": random.randint(item.win_rate_min, item.win_rate_max),
                "min_rate": item.win_rate_min,
                "max_rate": item.win_rate_max
            })

    return fake_user_lst


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
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('benefit_box')
        verbose_name_plural = _('benefit_boxes')
        db_table = 'benefit_box'

    def __str__(self):
        return '{}'.format(self.name)


class CommingSoonManager(models.Manager):
    def get_queryset(self):
        return super(CommingSoonManager, self).get_queryset().filter(coming_soon=True)


@python_2_unicode_compatible
class Unit(BaseUnit, Base):
    user = models.ManyToManyField(User, through='UserCard', related_name='units')
    heroes = models.ManyToManyField('Hero', through='HeroUnits', related_name='hero')
    unlock = models.BooleanField(_('unlock'), default=False, blank=True)
    coming_soon = models.BooleanField(_('coming soon'), default=False, blank=True)
    starting_unit = models.BooleanField(_('starting unit'), default=False, blank=True)
    history = HistoricalRecords()

    objects = models.Manager()
    unlock_coming_soon = CommingSoonManager()

    @classmethod
    def count(cls):
        return cls.objects.all().count()

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')
        db_table = 'unit'

    def __str__(self):
        return '{}'.format(self.moniker)


@python_2_unicode_compatible
class Hero(BaseUnit, Base):
    chakra_moniker = models.CharField(_('chakra moniker'), max_length=50)
    chakra_health = models.IntegerField(_('chakra health'), default=100)
    chakra_shield = models.IntegerField(_('chakra shield'), default=0)
    chakra_attack = models.IntegerField(_('chakra attack'), default=10)
    chakra_critical_chance = models.FloatField(_('chakra critical chance'), default=0.01)
    chakra_critical_ratio = models.FloatField(_('chakra critical ratio'), default=0.01)
    chakra_miss_chance = models.FloatField(_('chakra miss chance'), default=0.00)
    chakra_dodge_chance = models.FloatField(_('chakra dodge chance'), default=0.00)
    chakra_max_health = models.IntegerField(_('chakra max health'), default=100)
    chakra_max_shield = models.IntegerField(_('chakra max shield'), default=0)

    units = models.ManyToManyField(Unit, through='HeroUnits', related_name='hero')
    user = models.ManyToManyField(User, through='UserHero', related_name='hero')
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('hero')
        verbose_name_plural = _('heroes')
        db_table = 'hero'

    def __str__(self):
        return '{}'.format(self.moniker)


class UserBuy(Base):
    user = models.ForeignKey(User, related_name='user_buy')
    benefit = models.ForeignKey(BenefitBox, related_name='user_buy')
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('user_buy')
        verbose_name_plural = _('user_buy')
        db_table = 'user_buy'


@python_2_unicode_compatible
class UserCurrency(Base):
    name = models.CharField(_('name'), max_length=200, null=True)
    user = models.OneToOneField(User, related_name='user_currency')
    gem = models.PositiveIntegerField(_('gem quantity'), default=0)
    coin = models.PositiveIntegerField(_('coin quantity'), default=0)
    trophy = models.PositiveIntegerField(_('trophy quantity'), default=0)
    can_change_name = models.BooleanField(_('can change name'), default=True)
    session_count = models.PositiveIntegerField(_('session count'), default=0)
    need_comeback = models.BooleanField(_('nee comeback'), default=False)
    next_session_remaining_seconds = models.PositiveIntegerField(_('next session remaining seconds'), default=0)
    tutorial_done = models.BooleanField(_('tutorial'), default=False)
    ban_user = models.BooleanField(_('ban user'), default=False)
    win_count = models.PositiveIntegerField(_('win count'), default=0)
    lose_count = models.PositiveIntegerField(_('lose count'), default=0)

    google_account = models.CharField(_('google account'), max_length=200, null=True, blank=True, unique=True)
    google_id = models.CharField(_('google id'), max_length=200, null=True, blank=True, unique=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profile')
        db_table = 'profiles'

    @classmethod
    def hard_currency(cls, user):
        return cls.objects.get(user=user).gem

    @classmethod
    def soft_currency(cls, user):
        return cls.objects.get(user=user).coin

    @classmethod
    def subtract(cls, user, value, currency_type='COIN'):
        currency = cls.objects.get(user=user)

        if currency_type == 'GEM':
            currency.gem -= value

        else:
            currency.coin -= value

        currency.save()

    @classmethod
    def update_currency(cls, user, gems=0, coins=0):
        selected_user = cls.objects.get(user=user)

        if gems > 0:
            selected_user.gem += gems

        if coins > 0:
            selected_user.coin += coins

        selected_user.save()

    def __str__(self):
        return '{}'.format(self.name if self.name is not None else self.user.username)


@python_2_unicode_compatible
class HeroUnits(Base):
    hero = models.ForeignKey(Hero, related_name='units_hero')
    unit = models.ForeignKey(Unit, related_name='unit_heroes')
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('hero_unit')
        verbose_name_plural = _('hero_units')
        db_table = 'hero_units'
        unique_together = ('hero', 'unit')

    def __str__(self):
        return 'hero:{}, unit:{}'.format(self.hero.moniker, self.unit.moniker)


@python_2_unicode_compatible
class UserHero(Base):
    user = models.ForeignKey(User, related_name='user_hero', db_index=True)
    hero = models.ForeignKey(Hero, related_name='user_hero')
    enable_hero = models.BooleanField(_('enable hero'), default=False)
    quantity = models.PositiveIntegerField(_('quantity card'), default=0)
    level = models.PositiveIntegerField(_('level'), default=0)
    used_count = models.PositiveIntegerField(_('used count'), default=0)

    selected_item = JSONField(_('selected item'), null=True, default=None, blank=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('user_hero')
        verbose_name_plural = _('user_hero')
        db_table = 'user_hero'
        unique_together = ('user', 'hero')

    @classmethod
    def get_selected_item(cls, user, hero):
        lst_item = []
        try:
            user_hero = cls.objects.get(user=user, hero=hero)

            for item in user_hero.selected_item:
                lst_item.append(item['id'])

            return lst_item

        except:
            return lst_item

    def __str__(self):
        return 'user:{}, hero:{}'.format(self.user.username, self.hero.moniker)


class UnlockManager(models.Manager):
    def get_queryset(self):
        return super(UnlockManager, self).get_queryset().filter(character__unlock=True)


@python_2_unicode_compatible
class UserCard(Base):
    user = models.ForeignKey(User, verbose_name=_('username'), related_name='cards')
    character = models.ForeignKey(Unit, verbose_name=_('character'), related_name='cards')
    quantity = models.PositiveIntegerField(_('quantity card'), default=0)
    level = models.PositiveIntegerField(_('level'), default=1)
    cool_down = models.DateTimeField(_('cooldown'), null=True)
    cool_down_remaining_seconds = models.PositiveIntegerField(_('cool down remaining seconds'), default=0)
    used_quantity = models.PositiveIntegerField(_('used quantity'), default=0)

    history = HistoricalRecords()

    objects = models.Manager()
    unlock = UnlockManager()

    class Meta:
        verbose_name = _('user_card')
        verbose_name_plural = _('user_cards')
        db_table = 'user_card'
        unique_together = ('user', 'character')

    def __str__(self):
        return '{}'.format(self.quantity)

    @property
    def is_cool_down(self):
        try:
            cool_down_now_date = datetime.now(tz=pytz.utc)

            if cool_down_now_date <= self.cool_down:
                return True

            self.cool_down = None
            self.save()
            return False
        except Exception:
            return False

    @property
    def cool_down_remain_time(self):
        try:
            if self.cool_down:
                if datetime.now(tz=pytz.utc) > self.cool_down:
                    return 0

                return (self.cool_down - datetime.now(tz=pytz.utc)).total_seconds()

            return 0

        except Exception:
            return 0

    @property
    def skip_cooldown_gem(self):
        if self.cool_down:
            time_count = (self.cool_down - datetime.now(tz=pytz.utc)).total_seconds()
            if time_count == 0:
                return 0

            result = int(time_count / settings.COOL_DOWN_TIME)
            return 1 if result == 0 else result

    @classmethod
    def cards(cls, user):
        return cls.objects.filter(user=user).values_list('character')

    @classmethod
    def upgrade_character(cls, user, character, value):
        user_character = cls.objects.get(user=user, character=character)
        user_character.quantity += value
        if user_character.level == 0:
            user_character.level += 1

        user_character.save()


@python_2_unicode_compatible
class LeagueInfo(Base):
    name = models.CharField(_('name'), max_length=150)
    min_score = models.PositiveIntegerField(_('score for enter the league'), default=0)
    description = models.TextField(_('description'), null=True, default='')
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('league_info')
        verbose_name_plural = _('league_infoes')
        db_table = 'league_infoes'

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

    chest_type = models.CharField(_('chest type'), max_length=50, default='W', choices=CHEST_TYPE)
    info = models.ForeignKey(LeagueInfo, verbose_name=_('chest'), related_name='chests')
    min_coin = models.PositiveIntegerField(_('min coin'), default=0)
    max_coin = models.PositiveIntegerField(_('max coin'), default=0)
    min_gem = models.PositiveIntegerField(_('min gem'), default=0)
    max_gem = models.PositiveIntegerField(_('max gem'), default=0)
    new_card_chance = models.PositiveIntegerField(_('new card chance percentage'), default=1,
                                                  validators=[validate_percent])
    hero_card = models.PositiveIntegerField(_('hero card count'), default=0)
    unit_card = models.PositiveIntegerField(_('unit card count'), default=3)
    opening_time = models.PositiveIntegerField(_('opening time'), default=5)
    time_to_open = models.PositiveIntegerField(_('time to open'), default=2)
    history = HistoricalRecords()

    @classmethod
    def get(cls, chest_type):
        return Chest.objects.get(chest_type=chest_type, info__id=3)

    class Meta:
        verbose_name = _('chest')
        verbose_name_plural = _('chest')
        db_table = 'chest'
        unique_together = ('info', 'chest_type')

    def __str__(self):
        return '{}'.format(self.chest_type)


class Deck(models.Manager):
    def get_queryset(self):
        return super(Deck, self).get_queryset().exclude(status='used')


@python_2_unicode_compatible
class UserChest(Base):
    TYPE = (
        ('free', 'FREE'),
        ('non_free', 'NON_FREE')
    )

    STATUS = (
        ('close', 'close'),
        ('opening', 'opening'),
        ('ready', 'ready'),
        ('used', 'used')
    )

    user = models.ForeignKey(User, verbose_name=_('user'), related_name='chests')
    chest = models.ForeignKey(Chest, verbose_name=_('chest'), related_name='users')
    chest_monetaryType = models.CharField(_('chest type'), max_length=50, choices=TYPE, default='non_free')
    status = models.CharField(_('status'), max_length=50, choices=STATUS, default='close')
    sequence_number = models.PositiveIntegerField(_('sequence number'), default=0, validators=[validate_sequence])
    reward_data = JSONField(verbose_name=_('cards'), default=None, null=True)
    chest_opening_date = models.DateTimeField(_('chest opening time'), null=True, default=None)
    history = HistoricalRecords()

    objects = models.Manager()
    deck = Deck()

    @classmethod
    def reset_sequence(cls, user):
        cls.objects.filter(user=user).update(sequence_number=0)

    @classmethod
    def deck_is_open(cls, user, chest_type='free'):
        if cls.objects.filter(
                user=user,
                chest_monetaryType=chest_type,
        ).exclude(status='used').count() >= settings.DECK_COUNT[chest_type]:
            return False

        return True

    @property
    def skip_gem(self):
        if self.status == 'ready':
            return 0

        if not self.chest_opening_date:
            return 0

        current_time = timezone.now()

        if (self.chest_opening_date - timezone.now()).seconds >= 0:
            return (self.chest_opening_date - current_time).seconds / 300

    @property
    def remain_time(self):
        current_time = timezone.now()
        if self.chest_opening_date:
            if current_time > self.chest_opening_date:
                return 0

            return (self.chest_opening_date - current_time).seconds

        if self.chest_monetaryType == 'free':
            init_time = (datetime.now() + timedelta(seconds=5))

        else:
            init_time = (datetime.now() + timedelta(hours=settings.CHEST_SEQUENCE_TIME[self.chest.chest_type]))

        return (init_time - datetime.now()).seconds

    @property
    def chest_status(self):
        return self.status

    @property
    def initial_time(self):
        if self.chest_monetaryType == 'free':
            init_time = (datetime.now() + timedelta(seconds=5))

        else:
            init_time = (datetime.now() + timedelta(hours=settings.CHEST_SEQUENCE_TIME[self.chest.chest_type]))

        return (init_time - datetime.now()).seconds

    @chest_status.setter
    def chest_status(self, value):
        self.status = value

    @classmethod
    def get_sequence(cls, user):
        last_chest = cls.objects.filter(user=user).last()

        if last_chest is None:
            sequence_number = 0
            sequence_type = settings.CHEST_SEQUENCE[0]

        elif last_chest.sequence_number > len(settings.CHEST_SEQUENCE) -1:
            sequence_number = 0
            sequence_type = settings.CHEST_SEQUENCE[0]
            # cls.reset_sequence(user)

        else:
            sequence_number = last_chest.sequence_number
            sequence_type = settings.CHEST_SEQUENCE[last_chest.sequence_number]

        return sequence_number, sequence_type

    @classmethod
    def next_sequence(cls, user):
        last_chest = cls.objects.filter(user=user).last()

        if last_chest is None or last_chest.sequence_number > len(settings.CHEST_SEQUENCE) - 1:
            return 0

        else:
            return last_chest.sequence_number + 1

    class Meta:
        verbose_name = _('user_chest')
        verbose_name_plural = _('user_chest')
        db_table = 'user_chests'

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.chest.chest_type)


@python_2_unicode_compatible
class Item(Base):
    TYPE = (
        ('helmet', 'helmet'),
        ('weapon', 'weapon'),
        ('Armor', 'Armor'),
        ('Accessory_1', 'Accessory_1'),
        ('Accessory_2', 'Accessory_2'),
        ('Accessory_3', 'Accessory_3')
    )
    NAME = (
        ('Biker', 'Biker'),
        ('Dimetry', 'Dimetry'),
        ('Lion', 'Lion'),
        ('Guerrilla', 'Guerrilla'),
        ('Knight', 'Knight'),
        ('Horn', 'Horn'),
        ('Mexican', 'Mexican'),
        ('Naga', 'Naga'),
        ('Duff', 'Duff')
    )
    name = models.CharField(_('name'), max_length=50)
    damage = models.IntegerField(_('damage'), default=0)
    shield = models.IntegerField(_('shield'), default=0)
    health = models.IntegerField(_('health'), default=0)
    critical_ratio = models.FloatField(_('critical ratio'), default=0)
    critical_chance = models.FloatField(_('critical chance'), default=0)
    dodge_chance = models.FloatField(_('dodge chance'), default=0)
    item_type = models.CharField(_('item type'), max_length=50, null=True, default='helmet', choices=TYPE)
    level = models.PositiveIntegerField(_('level'), default=0)
    hero = models.ForeignKey(Hero, verbose_name=_('hero'), related_name='items')
    default_item = models.BooleanField(_('default'), default=False)

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
        unique_together = ('name', 'hero', 'item_type')
        db_table = 'items'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class UserItem(Base):
    user = models.ForeignKey(User, verbose_name=_('username'), related_name='items')
    item = models.ForeignKey(Item, verbose_name=_('item'), related_name='items')
    quantity = models.PositiveIntegerField(_('quantity card'), default=0)
    level = models.PositiveIntegerField(_('level'), default=0)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('user_item')
        verbose_name_plural = _('user_item')
        db_table = 'user_item'
        unique_together = ('user', 'item')

    def __str__(self):
        return '{}'.format(self.quantity)


@python_2_unicode_compatible
class HeroSpell(Base, Spell):
    hero = models.ForeignKey(Hero, verbose_name=_('hero'), related_name='spells')

    class Meta:
        verbose_name = _('chakra_spell')
        verbose_name_plural = _('hero_spells')
        db_table = 'hero_spells'

    def __str__(self):
        return '{}'.format(self.spell_name)


@python_2_unicode_compatible
class ChakraSpell(Base, Spell):
    hero = models.ForeignKey(Hero, verbose_name=_('hero'), related_name='chakra_spells')

    class Meta:
        verbose_name = _('chakra_spell')
        verbose_name_plural = _('chakra_spells')
        db_table = 'chakra_spells'

    def __str__(self):
        return '{}'.format(self.spell_name)


@python_2_unicode_compatible
class UnitSpell(Base, Spell):
    unit = models.ForeignKey(Unit, verbose_name=_('unit'), related_name='spells')

    class Meta:
        verbose_name = _('unit_spell')
        verbose_name_plural = _('unit_spells')
        db_table = 'unit_spells'

    def __str__(self):
        return '{}'.format(self.spell_name)


@python_2_unicode_compatible
class HeroSpellEffect(Base, SpellEffect):
    effect = models.ForeignKey(HeroSpell, verbose_name=_('effect'), related_name='effects')

    class Meta:
        verbose_name = _('hero_spell_effect')
        verbose_name_plural = _('hero_spell_effects')
        db_table = 'hero_spell_effects'

    def __str__(self):
        return '{}'.format(self.target_character_id)


@python_2_unicode_compatible
class ChakraSpellEffect(Base, SpellEffect):
    effect = models.ForeignKey(ChakraSpell, verbose_name=_('effect'), related_name='chakra_effects')

    class Meta:
        verbose_name = _('chakra_spell_effect')
        verbose_name_plural = _('chakra_spell_effects')
        db_table = 'chakra_spell_effects'

    def __str__(self):
        return '{}'.format(self.target_character_id)


@python_2_unicode_compatible
class UnitSpellEffect(Base, SpellEffect):
    effect = models.ForeignKey(UnitSpell, verbose_name=_('effect'), related_name='effects')

    class Meta:
        verbose_name = _('unit_spell_effect')
        verbose_name_plural = _('unit_spell_effects')
        db_table = 'unit_spell_effects'

    def __str__(self):
        return '{}'.format(self.target_character_id)


@python_2_unicode_compatible
class AppConfig(Base):
    app_data = JSONField(_('app config'), null=True, default=None)
    enable = models.BooleanField(_('enable'), default=False)

    class Meta:
        verbose_name = _('app_config')
        verbose_name_plural = _('app_configs')
        db_table = 'app_configs'

    def __str__(self):
        return '{}'.format(self.app_data)


@python_2_unicode_compatible
class Device(Base):
    user = models.ForeignKey(UserCurrency, verbose_name=_('user'), related_name='devices', null=True)
    device_model = models.CharField(_('device model'), max_length=100)
    device_id = models.CharField(_('device model'), max_length=500)

    class Meta:
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        db_table = 'devices'

    def __str__(self):
        return '{}-{}'.format(self.device_id, self.device_id)


@python_2_unicode_compatible
class Bot(Base):
    bot_name = models.CharField(_('bot name'), max_length=100, null=True, blank=True)
    min_trophy = models.IntegerField(_('min trophy'), null=True, blank=True)
    max_trophy = models.IntegerField(_('max trophy'), null=True, blank=True)
    sum_levels = models.IntegerField(_('sum levels'), null=True, blank=True)
    min_levels = models.IntegerField(_('min levels'), null=True, blank=True)
    max_levels = models.IntegerField(_('max levels'), null=True, blank=True)
    bot_ai = models.FloatField(_('bot ai'), null=True, blank=True)
    min_level_hero = models.IntegerField(_('min level hero'), null=True, blank=True)
    max_level_hero = models.IntegerField(_('max level hero'), null=True, blank=True)

    class Meta:
        verbose_name = _('bot')
        verbose_name_plural = _('bots')
        db_table = 'bots'

    def __str__(self):
        return '{}'.format(self.bot_name)


@python_2_unicode_compatible
class League(Base):
    LEAGUE_TYPE = (
        ('cooper', 'cooper'),
        ('bronze', 'bronze'),
        ('silver', 'silver'),
        ('gold', 'gold'),
        ('platinum', 'platinum'),
        ('diamond', 'diamond'),
    )
    league_name = models.CharField(_('league name'), max_length=250)
    capacity = models.PositiveIntegerField(_('capacity'), default=50)
    step_number = models.IntegerField(_('step number'), default=0, unique=True, db_index=True)
    league_type = models.CharField(_('league type'), max_length=10, choices=LEAGUE_TYPE, default='cooper')
    league_step = models.PositiveIntegerField(_('league step'), null=True, blank=True)
    min_trophy = models.IntegerField(_('min trophy'), null=True, blank=True, default=0)
    playoff_range = models.IntegerField(_('playoff range'), null=True, blank=True, default=0)
    playoff_count = models.IntegerField(_('playoff count'), null=True, blank=True, default=0)
    win_promoting_count = models.IntegerField(_('win promoting count'), null=True, blank=True, default=0)
    promoting_count = models.IntegerField(_('promoting count'), null=True, blank=True, default=0)
    demoting_count = models.IntegerField(_('demoting count'), null=True, blank=True, default=0)
    play_off_unlock_score = models.PositiveIntegerField(_('play off unlock score'), null=True, blank=True, default=0)
    play_off_start_gem = models.PositiveIntegerField(_('play off start gem '), null=True, blank=True, default=0)
    play_off_start_gem_1 = models.PositiveIntegerField(_('play off start gem 1'), null=True, blank=True, default=0)
    play_off_start_gem_2 = models.PositiveIntegerField(_('play off start gem 2'), null=True, blank=True, default=0)

    class Meta:
        verbose_name = _('league')
        verbose_name_plural = _('leagues')
        db_table = 'leagues'

    def __str__(self):
        return '{}'.format(self.league_name)


@python_2_unicode_compatible
class LeaguePrize(Base):
    gem = models.PositiveIntegerField(_('gem'), default=0)
    coin = models.PositiveIntegerField(_('coin'), default=0)
    level = models.PositiveIntegerField(_('level'), default=0)
    league = models.ForeignKey(League, verbose_name=_('league'), related_name='prizes')

    class Meta:
        verbose_name = _('prize')
        verbose_name_plural = _('prizes')
        db_table = 'prizes'
        unique_together = ('level', 'league')

    def __str__(self):
        return '{}'.format(self.id)


class EnableLeagueManager(models.Manager):
    def get_queryset(self):
        return super(EnableLeagueManager, self).get_queryset().filter(enable=True)


class CreatedLeague(Base):
    base_league = models.ForeignKey(League, verbose_name=_('league'), related_name='created_leagues')
    inc_count = models.PositiveIntegerField(_('inc count'), default=0)
    dec_count = models.PositiveIntegerField(_('dec count'), default=0)
    enable = models.BooleanField(_('enable legue'), default=True)

    objects = models.Manager()
    enable_leagues = EnableLeagueManager()

    class Meta:
        verbose_name = _('created_league')
        verbose_name_plural = _('created_leagues')
        db_table = 'created_leagues'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):

        if self.pk is None:
            self.params = {
                'fake_user': generate_fake_user_league(self.base_league)
            }

        super(CreatedLeague, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.id)

    def promoted(self):
        return LeagueUser.objects.filter(league=self).order_by('-score')[:LeagueTime.promoted()]

    def demoted(self):
        return LeagueUser.objects.filter(league=self).order_by('score')[:LeagueTime.promoted()]

    def promoted_list(self):
        lst_pro = []
        claim_count = 0
        claim = self.base_league.prizes.count() - 1

        for player in LeagueUser.objects.filter(league=self).in_league().order_by('-score')[:LeagueTime.promoted()]:
            promoted_league = League.objects.get(step_number=player.league.base_league.step_number + 1)

            lst_pro.append({
                "player": player.player,
                "league": promoted_league,
                "claim": self.base_league.prizes.all()[claim_count] if claim_count <= claim else None,
                "claim_league": player if claim_count <= claim else None,
                "type": "promoted"
            })
            claim_count += 1

        return lst_pro

    def demoted_list(self):
        lst_dmo = []
        for player in LeagueUser.objects.filter(league=self).in_league().order_by('score')[:LeagueTime.demoted()]:
            step_number = player.league.base_league.step_number - 1
            if step_number < 0:
                step_number = 0

            demoted_league = League.objects.get(step_number=step_number)
            lst_dmo.append({
                "player": player.player,
                "league": demoted_league,
                "claim": None,
                "claim_league": None,
                "type": "normal"
            })

        return lst_dmo

    def normal_list(self):
        lst_nor = []
        hi = list(LeagueUser.objects.filter(league=self)
                  .values_list('id', flat=True).in_league().order_by('-score')[:LeagueTime.promoted()])

        low = list(LeagueUser.objects.filter(league=self)
                   .values_list('id', flat=True).in_league().order_by('score')[:LeagueTime.demoted()])

        result = hi + low

        for player in LeagueUser.objects.filter(league=self).exclude(id__in=result).in_league():

            normal_league = League.objects.get(step_number=player.league.base_league.step_number)
            lst_nor.append({
                "player": player.player,
                "league": normal_league,
                "claim": None,
                "claim_league": None,
                "type": "normal"
            })

        return lst_nor

    def close(self):
        with transaction.atomic():
            self.enable = False
            self.save()

            for player in self.players.all():
                player.close_league = True
                player.save()

    @classmethod
    def create_or_join(cls, player, league, prize=None, league_player=None, type=None):
        leagues = cls.enable_leagues.filter(base_league=league)

        if leagues is not None:
            for find_league_league in leagues:
                if find_league_league.players.count() <= find_league_league.base_league.capacity:
                    selected_league = find_league_league
                    break
            else:
                selected_league = CreatedLeague.objects.create(base_league=league)

        else:
            selected_league = CreatedLeague.objects.create(base_league=league)

        if not LeagueUser.has_league(player):
            LeagueUser.objects.create(player=player, league=selected_league, league_change_status=type)

        if prize is not None and league_player is not None:
            Claim.prize(league_player=league_player, claim=prize)


class RandomManager(models.Manager):
    def get_queryset(self):
        return super(RandomManager, self).get_queryset().order_by('?')


class LeagueUserQuerySet(models.QuerySet):
    def in_league(self):
        return self.filter(close_league=False)


class LeagueUserManager(models.Manager):
    def get_queryset(self):
        return LeagueUserQuerySet(self.model, using=self._db)

    def in_league(self):
        return self.get_queryset().in_league()


class LeagueUser(Base):
    PLAY_OFF_STATUS = (
        ('disable', 'disable'),
        ('not_started', 'not_started'),
        ('start', 'start'),
    )
    LEAGUE_STATUS = (
        ('normal', 'normal'),
        ('promoted', 'promoted'),
        ('demoted', 'demoted'),
    )

    player = models.ForeignKey(UserCurrency, verbose_name=_('player'), related_name='leagues')
    league = models.ForeignKey(CreatedLeague, verbose_name=_('created_leagues'), related_name='players')
    score = models.PositiveIntegerField(_('score'), default=0)
    rank = models.PositiveIntegerField(_('rank'), blank=True, null=True)
    close_league = models.BooleanField(_('close'), default=False)
    play_off_count = models.PositiveIntegerField(_('play off count'), default=0)
    lose_count = models.PositiveIntegerField(_('lose count'), default=0)
    play_off_status = models.CharField(_('play off status'), max_length=50, choices=PLAY_OFF_STATUS, default='disable')
    match_count = models.PositiveIntegerField(_('match count'), default=0)
    league_change_status = models.CharField(_('league change status'), max_length=50,
                                            choices=LEAGUE_STATUS, default='normal')

    objects = LeagueUserManager()
    randoms = RandomManager()

    class Meta:
        verbose_name = _('league_user')
        verbose_name_plural = _('league_user')
        db_table = 'league_user'
        unique_together = ('player', 'league')

    def __unicode__(self):
        return '{}-{}'.format(self.player.name, self.league.base_league.league_name)

    @classmethod
    def has_league(cls, player):
        if cls.objects.filter(player=player, close_league=False):
            return True

        return False

    @classmethod
    def player_score(cls, player):
        try:
            league_user = cls.objects.get(player=player, close_league=False)
            if league_user:
                return league_user.score

            return 0

        except:
            return 0

    @classmethod
    def create_or_join_league(cls, player, selected_league):
        try:
            if cls.objects.filter(player=player, close_league=False).count() == 0:

                created_leagues = CreatedLeague.objects.values('id').annotate(user_count=Count('players')).filter(
                    user_count__lte=selected_league.capacity, base_league=selected_league)

                if len(created_leagues) > 0:
                    random_league = random.randint(0, len(created_leagues)-1)
                    find_league = CreatedLeague.objects.get(pk=created_leagues[random_league]['id'])

                    LeagueUser.objects.create(
                        player=player,
                        league=find_league
                    )

                else:
                    created_league = CreatedLeague.objects.create(base_league=selected_league)
                    LeagueUser.objects.create(
                        player=player,
                        league=created_league
                    )

                return True

            return False

        except Exception:
            return False


class EnableManager(models.Manager):
    def get_queryset(self):
        return super(EnableManager, self).get_queryset().filter(enable=True)


class PlayOff(Base):
    STATUS = (
        ('win', 'win'),
        ('lose', 'lose')
    )

    status = models.CharField(_('status'), max_length=5, choices=STATUS, default='win')
    player_league = models.ForeignKey(LeagueUser, verbose_name=_('player'), related_name='logs')
    enable = models.BooleanField(_('enable'), default=True)

    objects = models.Manager()
    enabled = EnableManager()

    class Meta:
        verbose_name = _('playoff')
        verbose_name_plural = _('playoffs')
        db_table = 'playoff'

    def __unicode__(self):
        return 'playoff-{}'.format(self.player_league.player.name.encode('utf-8'))

    @classmethod
    def reset(cls, player):
        try:
            league_user = LeagueUser.objects.get(player=player, play_off_status='start')
            league_user.play_off_count = 0
            league_user.save()
            cls.objects.filter(player_league=league_user).update(enable=False)
            return True

        except Exception:
            return False

    @classmethod
    def log(cls, player):
        try:
            league = LeagueUser.objects.get(player=player, play_off_status='start', close_league=False)
            playoff_log = PlayOff.enabled.filter(player_league=league)

            if playoff_log.count() > league.league.base_league.playoff_count:
                return -1

            result = []
            for log in playoff_log.all().order_by('id'):
                if log.status == 'win':
                    result.append(1)

                else:
                    result.append(0)

            remain_playoff = league.league.base_league.playoff_count - len(result)
            if remain_playoff > 0:
                for i in range(0, remain_playoff):
                    result.append(2)

            return result

        except LeagueUser.DoesNotExist:
            return []

    @classmethod
    def wins(cls, player):
        league = LeagueUser.objects.get(player=player, play_off_status='start')
        playoff_log = PlayOff.enabled.filter(player_league=league, status='win')
        return playoff_log.count()

    @classmethod
    def loses(cls, player):
        league = LeagueUser.objects.get(player=player, play_off_status='start')
        playoff_log = PlayOff.enabled.filter(player_league=league, status='lose')
        return playoff_log.count()


class Claim(Base):
    coin = models.PositiveIntegerField(_('coin'), default=10)
    gem = models.PositiveIntegerField(_('gem'), default=10)
    is_used = models.BooleanField(_('used'), default=False)
    league_player = models.ForeignKey(LeagueUser, verbose_name=_('league_user'), related_name="claims", db_index=True)

    class Meta:
        verbose_name = _('claim')
        verbose_name_plural = _('claims')
        db_table = 'claims'

    def __str__(self):
        return 'claim-{}'.format(self.league_player.league.base_league.league_name)

    @classmethod
    def prize(cls, league_player=None, claim=None):
        if claim is not None and league_player is not None:
            cls.objects.filter(league_player=league_player).delete()
            cls.objects.create(league_player=league_player, gem=claim.gem, coin=claim.coin)


class LeagueTime(Base):
    end_date = models.DateTimeField(_('global end date'))
    expired = models.BooleanField(_('leagues expired'), default=False)
    promoting_count = models.PositiveIntegerField(_('promoting count'), default=3)
    demoting_count = models.PositiveIntegerField(_('demoting count'), default=3)

    class Meta:
        verbose_name = _('league time')
        verbose_name_plural = _('league_times')
        db_table = 'league_times'

    def __str__(self):
        return 'league-{}'.format(self.id)

    @classmethod
    def remain_time(cls):
        league = cls.objects.get(expired=False)

        if league.end_date > datetime.now(tz=pytz.utc):
            return int((league.end_date - datetime.now(tz=pytz.utc)).total_seconds())

        return 0

    @classmethod
    def reset(cls):
        with transaction.atomic():
            league = cls.objects.get(expired=False)
            league.expired = True
            league.save()
            cls.objects.create(end_date=datetime.now(tz=pytz.utc) + timedelta(days=settings.LEAGUE_LENGTH))

    @classmethod
    def promoted(cls):
        league = cls.objects.get(expired=False)
        return league.promoting_count

    @classmethod
    def demoted(cls):
        league = cls.objects.get(expired=False)
        return league.demoting_count


class FakeQuerySet(models.QuerySet):
    def enable(self):
        return self.filter(enable=True)


class FakeManager(models.Manager):
    def get_queryset(self):
        return FakeQuerySet(self.model, using=self._db)

    def enable(self):
        return self.get_queryset().enable()


@python_2_unicode_compatible
class Fake(Base):
    name = models.CharField(_('fake description'), max_length=50, null=True, blank=True)
    league = models.ForeignKey(League, verbose_name=_('league'), related_name='fakes')
    enable = models.BooleanField(_('enable'), default=True)

    objects = FakeManager()

    class Meta:
        verbose_name = _('fake')
        verbose_name_plural = _('fakes')
        db_table = 'fakes'

    def __str__(self):
        return 'fake-{}'.format(self.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        Fake.objects.filter(league=self.league).update(enable=False)
        super(Fake, self).save(*args, **kwargs)

    @classmethod
    def valid_quantity(cls, fake_id, exclude_lst, value):
        fake = cls.objects.get(pk=fake_id)
        detail_sum = fake.details.exclude(id__in=exclude_lst).aggregate(Sum('quantity'))

        if detail_sum['quantity__sum'] + value <= fake.league.capacity:
            return True

        return False


@python_2_unicode_compatible
class FakeDetail(Base):
    TYPE_STATUS = (
        ('promote', 'promote'),
        ('normal', 'normal'),
        ('demote', 'demote'),
    )
    quantity = models.PositiveIntegerField(_('quantity'), default=5)
    win_rate_min = models.PositiveIntegerField(_('win rate min percent'))
    win_rate_max = models.PositiveIntegerField(_('win rate max percent'))
    type = models.CharField(_('type'), max_length=10, choices=TYPE_STATUS)
    fake = models.ForeignKey(Fake, verbose_name=_('fake'), related_name='details')

    class Meta:
        unique_together = ('type', 'fake')
        verbose_name = _('fake_detail')
        verbose_name_plural = _('fake_details')
        db_table = 'fake_details'

    def __str__(self):
        return 'fake-{}-{}-{}'.format(self.fake.name, self.type, self.quantity)

    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('field1', 'field2'):
            return 'type duplicated !!!'
        else:
            return super(FakeDetail, self).unique_error_message(model_class, unique_check)


def create_user_dependency(sender, instance, created, **kwargs):
    if created:
        for unit in Unit.objects.all():
            if unit.starting_unit:
                UserCard.objects.create(user=instance, character=unit, quantity=1)

            else:
                UserCard.objects.create(user=instance, character=unit, level=0)

        for item in Item.objects.all():
            UserItem.objects.create(item=item, user=instance)

        for hero in Hero.objects.all():
            UserHero.objects.get_or_create(user=instance, hero=hero)

        UserCurrency.objects.create(user=instance, gem=100, coin=250)


def assigned_new_card_to_user(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            UserItem.objects.create(user=user, item=instance)


signals.post_save.connect(create_user_dependency, sender=User)

signals.post_save.connect(assigned_new_card_to_user, sender=Item)
