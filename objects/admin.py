# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import BenefitBox, Unit, Hero, HeroUnits, LeagueInfo, Chest, Item, UserHero, HeroSpell, HeroSpellEffect, \
    UnitSpell, UnitSpellEffect, ChakraSpell, ChakraSpellEffect, UserCurrency, AppConfig
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User
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


class ItemInline(admin.StackedInline):
    model = Item
    fields = (
        'name',
        'damage' ,
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
    search_fields = ['username']
    list_filter = ['is_staff']
    inlines = [UserCurrencyInline]


@admin.register(BenefitBox)
class BenefitBoxAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'box', 'quantity', 'flag_api')
    list_filter = ('flag_api', 'box')
    # history_list_display = ['name', 'box', 'quantity', 'flag_api']


@admin.register(Unit)
class UnitAdmin(SimpleHistoryAdmin):
    list_display = ('moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start', 'unlock')
    list_editable = ('unlock', )
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