# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from objects.models import League, Unit, Hero, UserCurrency, UnitSpell
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.db.models import signals
from base import fields
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import user_logged_in
from common.network import get_client_ip
from django.dispatch import receiver

import uuid
import pytz


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

    MUST_HAVE_TYPE = (
        ('random', 'random'),
        ('all', 'all')
    )

    chest_type = models.CharField(_('chest type'), max_length=50, default='W', choices=CHEST_TYPE)
    league = models.ForeignKey(League, verbose_name=_('league'), related_name='ctm_chests')

    min_coin = models.PositiveIntegerField(_('min coin'), default=0)
    max_coin = models.PositiveIntegerField(_('max coin'), default=0)

    min_gem = models.PositiveIntegerField(_('min gem'), default=0)
    max_gem = models.PositiveIntegerField(_('max gem'), default=0)

    total = models.PositiveIntegerField(_('total'), default=0)
    card_try = models.PositiveIntegerField(_('count try'), default=0)

    epic_chance = models.PositiveIntegerField(_('epic chance'), default=0)
    min_epic = models.PositiveIntegerField(_('min epic'), default=0)
    max_epic = models.PositiveIntegerField(_('max epic'), default=0)

    rare_chance = models.PositiveIntegerField(_('rare chance'), default=0)
    min_rare = models.PositiveIntegerField(_('min rare'), default=0)
    max_rare = models.PositiveIntegerField(_('max rare'), default=0)

    is_must_have_hero = models.BooleanField(_('is must have hero'), default=False)
    must_have_hero_type = models.CharField(_('must have hero type'), max_length=10, default='random',
                                           choices=MUST_HAVE_TYPE)
    min_have_hero = models.PositiveIntegerField(_('min have hero'), default=0)
    max_have_hero = models.PositiveIntegerField(_('max have hero'), default=0)
    must_have_hero = models.ManyToManyField(Hero, verbose_name=_('must have hero'), blank=True)

    is_must_have_spell = models.BooleanField(_('is must have spell'), default=False)
    must_have_spell_type = models.CharField(_('must have spell type'), max_length=10, default='random',
                                            choices=MUST_HAVE_TYPE)
    min_have_spell = models.PositiveIntegerField(_('min have spell'), default=0)
    max_have_spell = models.PositiveIntegerField(_('max have spell'), default=0)
    must_have_spell = models.ManyToManyField(UnitSpell, verbose_name=_('must have unit spell'), blank=True)

    is_must_have_troop = models.BooleanField(_('is must have troop'), default=False)
    min_have_troop = models.PositiveIntegerField(_('min have spell'), default=0)
    max_have_troop = models.PositiveIntegerField(_('max have spell'), default=0)
    must_have_troop = models.ManyToManyField(Unit, verbose_name=_('must have troop'), blank=True)
    must_have_troop_type = models.CharField(_('must have troop type'), max_length=10, default='random',
                                            choices=MUST_HAVE_TYPE)

    class Meta:
        verbose_name = _('ctm')
        verbose_name_plural = _('ctm')
        db_table = 'ctm'
        unique_together = ('chest_type', 'league')

    def __str__(self):
        return '{}-{}'.format(self.chest_type, self.league.league_name)

    @classmethod
    def chest_total_card(cls, league):
        result = {}
        for item in cls.objects.filter(league=league):
            result[item.get_chest_type_display()] = item.total

        return result


# @python_2_unicode_compatible
# class CtmMustHaveHero(Base):
#     ctm = models.ForeignKey(CTM, verbose_name=_('ctm'))
#     hero = models.ForeignKey(Hero, verbose_name=_('hero'))
#
#     class Meta:
#         verbose_name = _('ctm_must_have_hero')
#         verbose_name_plural = _('ctm_must_have_heroes')
#         db_table = 'ctm_must_have_heroes'
#         unique_together = ('ctm', 'hero')
#
#     def __str__(self):
#         return '{}-{}'.format(self.ctm, self.hero)
#
#
# @python_2_unicode_compatible
# class CtmMustHaveSpell(Base):
#     ctm = models.ForeignKey(CTM, verbose_name=_('ctm'))
#     spell = models.ForeignKey(Spell, verbose_name=_('spell'))
#
#     class Meta:
#         verbose_name = _('ctm_must_have_spell')
#         verbose_name_plural = _('ctm_must_have_spells')
#         db_table = 'ctm_must_have_spells'
#         unique_together = ('ctm', 'spell')
#
#     def __str__(self):
#         return '{}-{}'.format(self.ctm, self.spell)


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


@python_2_unicode_compatible
class CustomBot(Base):
    bot_name = models.CharField(_('bot name'), max_length=200)
    enable = models.BooleanField(_('enable'), default=False)
    hero = models.ForeignKey(Hero, verbose_name=_('hero'), related_name='bots', null=True, blank=True)
    level = models.PositiveIntegerField(_('level'), default=1)

    units = models.ManyToManyField(Unit, verbose_name=_('units'), through='CustomBotTroop', related_name='bots')

    class Meta:
        verbose_name = _('custom_bot')
        verbose_name_plural = _('custom_bots')
        db_table = 'custom_bots'

    def __str__(self):
        return '{}'.format(self.bot_name)

    @property
    def troops(self):
        result = None

        for troop in self.troops:
            result = "{},".join(troop)

        return result


class CustomBotTroop(Base):
    troop = models.ForeignKey(Unit, verbose_name=_('troop'), related_name='custom_bots')
    bot = models.ForeignKey(CustomBot, verbose_name=_('bot'), related_name='troops')
    level = models.PositiveIntegerField(_('level'), validators=[MaxValueValidator(10), MinValueValidator(0)])

    class Meta:
        verbose_name = _('custom_bot_troop')
        verbose_name_plural = _('custom_bot_troops')
        db_table = 'custom_bot_troops'
        unique_together = ('troop', 'bot')

    def __str__(self):
        return '{}'.format(self.bot.bot_name)


class CustomTokenQuerySet(models.QuerySet):
    def enable(self):
        return self.filter(enable=True)


class CustomTokenManager(models.Manager):
    def get_queryset(self):
        return CustomTokenQuerySet(self.model, using=self._db)

    def enable(self):
        return self.get_queryset().enable()


class CustomToken(Base):
    token_desc = models.CharField(_('token description'), max_length=50, blank=True, null=True)
    gem_reward = models.PositiveIntegerField(_('gem reward'), default=1000)
    coin_reward = models.PositiveIntegerField(_('coin reward'), default=1000)
    token = models.CharField(_('token'), max_length=200, unique=True, blank=True)
    expire_date = models.DateTimeField(_('expire date'), blank=True, null=True)
    enable = models.BooleanField(_('enable'), default=False)

    objects = CustomTokenManager()

    class Meta:
        verbose_name = _('custom_token')
        verbose_name_plural = _('custom_tokens')
        db_table = 'custom_tokens'

    def __str__(self):
        return '{}'.format(self.token)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.pk is None:
            self.token = str(uuid.uuid4())
            self.expire_date = datetime.now() + timedelta(days=settings.TOKEN_ADDITIONAL_TIME)

        super(CustomToken, self).save()

    @classmethod
    def is_valid(cls, token):
        custom_token = cls.objects.enable().filter(token=token).first()

        if custom_token is None:
            return False

        else:
            if custom_token.expire_date > datetime.now(tz=pytz.utc):
                return True

            return False


@python_2_unicode_compatible
class UserLoginActivity(models.Model):
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = (
        (SUCCESS, 'Success'),
        (FAILED, 'Failed')
    )

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)
    player = models.ForeignKey(UserCurrency, verbose_name=_('player'), null=True, blank=True, related_name='login_logs')

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'
        db_table = 'user_login_activities'

    def __str__(self):
        return "{}-{}".format(self.login_IP, self.login_username)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        if self.pk is None:
            player = UserCurrency.objects.get(user__username=self.login_username)
            self.player = player

        super(UserLoginActivity, self).save(*args, **kwargs)


def assigned_item_to_ctm(sender, instance, created, **kwargs):
    if created:
        for unit in Unit.objects.all():
            CTMUnit.objects.create(unit=unit, ctm=instance)

        for hero in Hero.objects.all():
            CTMHero.objects.create(hero=hero, ctm=instance)


@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255],
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=user.username,
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        print "log_user_logged_in request: {}, error: {}".format(request, e)


signals.post_save.connect(assigned_item_to_ctm, sender=CTM)
