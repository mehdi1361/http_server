# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import BenefitBox, Unit, Hero, HeroUnits, LeagueInfo, Chest, Item, UserHero, HeroSpell, HeroSpellEffect, \
    UnitSpell, UnitSpellEffect, ChakraSpell, ChakraSpellEffect, UserCurrency, AppConfig, Bot
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User
from shopping.models import CurrencyLog, PurchaseLog
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


class ChestInline(admin.StackedInline):
    model = Chest


class HeroSpellEffectInline(admin.TabularInline):
    model = HeroSpellEffect


class UnitSpellEffectInline(admin.TabularInline):
    model = UnitSpellEffect


class ChakraSpellEffectInline(admin.TabularInline):
    model = ChakraSpellEffect


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
class UserCurrency(admin.ModelAdmin):
    list_display = ['name', 'gem', 'coin', 'trophy', 'player_id', 'ban_user']
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
        'bot_ai'
    )
    list_editable = (
        'min_trophy',
        'max_trophy',
        'sum_levels',
        'min_levels',
        'max_levels',
        'bot_ai'
    )