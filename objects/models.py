# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from multiselectfield.db.fields import MultiSelectField

from base.models import Base, BaseUnit, Spell, SpellEffect
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models import signals
from .validators import validate_percent, validate_sequence
from django.conf import settings
from django.contrib.postgres.fields import JSONField, ArrayField
from simple_history.models import HistoricalRecords
from django.utils import timezone
from datetime import datetime, timedelta
# from multiselectfield import MultiSelectField


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


@python_2_unicode_compatible
class Unit(BaseUnit, Base):
    user = models.ManyToManyField(User, through='UserCard', related_name='units')
    heroes = models.ManyToManyField('Hero', through='HeroUnits', related_name='hero')
    history = HistoricalRecords()

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
        return '{}, gem:{}, coin:{}'.format(self.user, self.gem, self.coin)


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
    selected_item = JSONField(_('selected item'), null=True, default=None)
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


@python_2_unicode_compatible
class UserCard(Base):
    user = models.ForeignKey(User, verbose_name=_('username'), related_name='cards')
    character = models.ForeignKey(Unit, verbose_name=_('character'), related_name='cards')
    quantity = models.PositiveIntegerField(_('quantity card'), default=0)
    level = models.PositiveIntegerField(_('level'), default=1)
    cool_down = models.DateTimeField(_('cooldown'), null=True)
    cool_down_remaining_seconds = models.PositiveIntegerField(_('cool down remaining seconds'), default=0)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('user_card')
        verbose_name_plural = _('user_cards')
        db_table = 'user_card'
        unique_together = ('user', 'character')

    def __str__(self):
        return '{}'.format(self.quantity)

    @property
    def is_cool_down(self):
        cool_down_now_date = timezone.now()

        if cool_down_now_date < (self.cool_down if self.cool_down else cool_down_now_date):
            return True
        return False

    @classmethod
    def cards(cls, user):
        return cls.objects.filter(user=user).values_list('character')

    @classmethod
    def upgrade_character(cls, user, character, value):
        user_character = cls.objects.get(user=user, character=character)
        user_character.quantity += value
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
    def deck_is_open(cls, user, chest_type):
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
            return (self.chest_opening_date - current_time).seconds / 60

    @property
    def remain_time(self):
        current_time = timezone.now()
        if self.chest_opening_date:
            return (self.chest_opening_date - current_time).seconds

        init_time = (datetime.now() + timedelta(hours=settings.CHEST_SEQUENCE_TIME[self.chest.chest_type]))
        return (init_time - datetime.now()).seconds

    @property
    def chest_status(self):
        return self.status
    
    @property
    def initial_time(self):
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
            cls.reset_sequence(user)

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
        ('Accessory', 'Accessory')
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


def create_user_dependency(sender, instance, created, **kwargs):
    if created:
        for unit in Unit.objects.all():
            UserCard.objects.create(user=instance, character=unit)

        for item in Item.objects.all():
            UserItem.objects.create(item=item, user=instance)

        for hero in Hero.objects.all():
            UserHero.objects.get_or_create(user=instance, hero=hero)

        UserCurrency.objects.create(user=instance)


def assigned_new_card_to_user(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            UserItem.objects.create(user=user, item=instance)


signals.post_save.connect(create_user_dependency, sender=User)

signals.post_save.connect(assigned_new_card_to_user, sender=Item)
