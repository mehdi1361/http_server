# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import  messages
from django.contrib import admin
from .models import BenefitBox, Unit, Hero, HeroUnits, LeagueInfo, Chest, Item, UserHero, HeroSpell, HeroSpellEffect, \
    UnitSpell, UnitSpellEffect, ChakraSpell, ChakraSpellEffect, UserCurrency, AppConfig, Bot, \
    League, LeagueUser, CreatedLeague, LeaguePrize, Claim, PlayOff, LeagueTime, Fake, FakeDetail
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User
from shopping.models import CurrencyLog, PurchaseLog
from django.forms.models import BaseInlineFormSet
# from django.contrib.auth.models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_staff', 'is_superuser')

admin.site.unregister(User)


class UserCurrencyInline(admin.StackedInline):
    model = UserCurrency
    max_num = 1
    can_delete = False


class HeroUnitsAdmin(admin.StackedInline):
    model = HeroUnits


class PurchaseLogAdmin(admin.TabularInline):
    model = PurchaseLog


class CurrencyLogAdmin(admin.TabularInline):
    model = CurrencyLog


class LeagueUserAdmin(admin.TabularInline):
    model = LeagueUser


class LeaguePrizeAdmin(admin.StackedInline):
    model = LeaguePrize


class ItemInline(admin.StackedInline):
    model = Item
    fields = (
        'name',
        'damage',
        'shield',
        'health',
        'critical_ratio',
        'dodge_chance',
        'item_type',
        'level',
        'hero',
        'default_item'
    )


class ClaimInline(admin.StackedInline):
    model = Claim


class ChestInline(admin.StackedInline):
    model = Chest


class HeroSpellEffectInline(admin.TabularInline):
    model = HeroSpellEffect


class UnitSpellEffectInline(admin.TabularInline):
    model = UnitSpellEffect


class ChakraSpellEffectInline(admin.TabularInline):
    model = ChakraSpellEffect


# class FakeDetailInlineFormSet(BaseInlineFormSet):
#     def save_new_objects(self, commit=True):
#         save_instance = super(FakeDetailInlineFormSet, self).save_new_objects(commit)
#         if commit:
#             for item in save_instance:
#                 print item
#
#         return save_instance
#
#     def save_existing_objects(self, commit=True):
#         save_instance = super(FakeDetailInlineFormSet, self).save_existing_objects(commit)
#         if commit:
#             sum_val = 0
#             exclude_lst = []
#             fake = None
#             for item in save_instance:
#                 sum_val += item.quantity
#                 exclude_lst.append(item.id)
#                 fake = item.fake
#
#             if Fake.valid_quantity(fake.id, exclude_lst, sum_val):
#                 return save_instance
#
#             else:
#                 messages.add_message()


class FakeDetailInline(admin.TabularInline):
    model = FakeDetail

    def save_formset(self, request, form, formset, change):
        print self


@admin.register(User)
class AccountsUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'last_login']
    search_fields = ['username', ]
    list_filter = ['is_staff']
    inlines = [UserCurrencyInline]


    # def get_name(self, obj):
    #     profile = UserCurrency.objects.filter(user=obj)
    #     return profile.name


@admin.register(UserCurrency)
class UserCurrencyAdmin(admin.ModelAdmin):
    list_display = ['name', 'gem', 'coin', 'trophy', 'player_id', 'win_count', 'lose_count', 'ban_user']
    list_editable = ['ban_user']
    search_fields = ['name']
    inlines = [PurchaseLogAdmin, CurrencyLogAdmin]

    def player_id(self, obj):
        return obj.user.username


@admin.register(BenefitBox)
class BenefitBoxAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'box', 'quantity', 'flag_api')
    list_filter = ('flag_api', 'box')
    # history_list_display = ['name', 'box', 'quantity', 'flag_api']


@admin.register(Unit)
class UnitAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'moniker', 'health', 'shield', 'attack', 'dexterity', 'starting_unit', 'unlock')
    list_editable = ('unlock', 'starting_unit')
    # history_list_display = ['moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start']
    list_filter = ('dexterity', )

    def get_form(self, request, obj=None, **kwargs):

        self.exclude = ("max_health", "max_shield")
        form = super(UnitAdmin, self).get_form(request, obj, **kwargs)
        return form


@admin.register(Hero)
class HeroAdmin(SimpleHistoryAdmin):
    list_display = ('moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start')
    list_filter = ('dexterity', )
    inlines = (HeroUnitsAdmin, ItemInline)


@admin.register(LeagueInfo)
class LeagueInfoAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'min_score', 'description', 'created_date', 'updated_date')
    # history_list_display = ['name', 'min_score', 'description', 'created_date', 'updated_date']
    inlines = (ChestInline, )


@admin.register(Item)
class ItemAdmin(SimpleHistoryAdmin):
    list_display = (
        'id',
        'name',
        'hero',
        'item_type',
        'damage',
        'shield',
        'health',
        'critical_ratio',
        'critical_chance',
        'dodge_chance',
        'created_date',
        'updated_date'
    )
    readonly_fields = ('level', )
    ordering = ('id', )


@admin.register(UserHero)
class UserHeroAdmin(SimpleHistoryAdmin):
    list_display = (
        'user',
        'hero',
        'enable_hero',
        'quantity',
        'level',
        'selected_item'
    )
    search_fields = ("user__username", )


@admin.register(HeroSpell)
class HeroSpellAdmin(SimpleHistoryAdmin):
    list_display = (
        'spell_name',
        'hero',
        'spell_type',
        'action_type',
        'need_action_point',
        'cool_down_duration',
        'char_spells_index',
        'generated_action_point',
    )

    inlines = (HeroSpellEffectInline, )


@admin.register(UnitSpell)
class UnitSpellAdmin(SimpleHistoryAdmin):
    list_display = (
        'spell_name',
        'unit',
        'spell_type',
        'action_type',
        'need_action_point',
        'cool_down_duration',
        'char_spells_index',
        'generated_action_point',
    )

    inlines = (UnitSpellEffectInline, )


@admin.register(ChakraSpell)
class ChakraSpellAdmin(SimpleHistoryAdmin):
    list_display = (
        'spell_name',
        'hero',
        'spell_type',
        'action_type',
        'need_action_point',
        'cool_down_duration',
        'char_spells_index',
        'generated_action_point',
    )

    inlines = (ChakraSpellEffectInline, )


@admin.register(AppConfig)
class AppConfig(admin.ModelAdmin):
    list_display = (
        'app_data',
        'enable'
    )


@admin.register(Chest)
class ChestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'chest_type',
        'info',
        'min_coin',
        'max_coin',
        'min_gem',
        'max_gem',
        'new_card_chance',
        'hero_card',
        'unit_card',
        'opening_time',
        'time_to_open'
    )
    list_editable = (
        'chest_type',
        'info',
        'min_coin',
        'max_coin',
        'min_gem',
        'max_gem',
        'new_card_chance',
        'hero_card',
        'unit_card',
        'opening_time',
        'time_to_open'
    )


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = (
        'bot_name',
        'min_trophy',
        'max_trophy',
        'sum_levels',
        'min_levels',
        'max_levels',
        'bot_ai',
        'min_level_hero',
        'max_level_hero'
    )
    list_editable = (
        'min_trophy',
        'max_trophy',
        'sum_levels',
        'min_levels',
        'max_levels',
        'bot_ai',
        'min_level_hero',
        'max_level_hero'
    )


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        'league_name',
        'capacity',
        'step_number',
        'league_type',
        'min_trophy',
        'playoff_range',
        'playoff_count',
        'win_promoting_count',
        'promoting_count',
        'demoting_count',
        'play_off_unlock_score',
        'play_off_start_gem',
        'play_off_start_gem_1',
        'play_off_start_gem_2'
    )
    list_editable = (
        'capacity',
        'step_number',
        'league_type',
        'min_trophy',
        'playoff_range',
        'playoff_count',
        'win_promoting_count',
        'promoting_count',
        'demoting_count',
        'play_off_unlock_score',
        'play_off_start_gem',
        'play_off_start_gem_1',
        'play_off_start_gem_2'
    )
    ordering = ('step_number', )
    inlines = (LeaguePrizeAdmin, )


@admin.register(CreatedLeague)
class CreatedLeagueAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'base_league',
        'inc_count',
        'dec_count',
        'created_date',
        'updated_date',
        'enable'
    )

    list_editable = (
        'base_league',
        'inc_count',
        'dec_count',
        'enable'
    )
    inlines = [LeagueUserAdmin, ]


@admin.register(LeagueUser)
class LeagueUserAdmin(admin.ModelAdmin):
    # readonly_fields = (
    #     'player',
    #     'league',
    #     'score',
    #     'close_league',
    #     'rank',
    #     'play_off_count',
    #     'lose_count',
    #     'play_off_status',
    #     'match_count',
    #     'league_change_status'
    # )
    list_display = (
        'player',
        'league',
        'score',
        'close_league',
        'rank',
        'play_off_count',
        'lose_count',
        'play_off_status',
        'match_count',
        'league_change_status'
    )

    list_editable = (
        'score',
    )
    inlines = (ClaimInline, )


@admin.register(PlayOff)
class PlayOffAdmin(admin.ModelAdmin):
    list_display = (
        'player_league',
        'status',
        'created_date',
        'updated_date',
        'enable'
    )


@admin.register(LeagueTime)
class LeagueTimeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'end_date',
        'expired',
        'promoting_count',
        'demoting_count',
        'created_date',
        'updated_date'
    )

    list_editable = (
        'end_date',
        'expired',
        'promoting_count',
        'demoting_count'
    )


@admin.register(Fake)
class FakeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'league',
        'enable'
    )

    list_editable = (
        'enable',
    )

    inlines = (FakeDetailInline, )

