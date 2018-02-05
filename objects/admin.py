# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import BenefitBox, Unit, Hero, HeroUnits, LeagueInfo, Chest, Item, UserHero
from simple_history.admin import SimpleHistoryAdmin
# from django.contrib.auth.models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_staff', 'is_superuser')


class HeroUnitsAdmin(admin.StackedInline):
    model = HeroUnits


class ItemInline(admin.StackedInline):
    model = Item


class ChestInline(admin.StackedInline):
    model = Chest


@admin.register(BenefitBox)
class BenefitBoxAdmin(SimpleHistoryAdmin):
    list_display = ('name', 'box', 'quantity', 'flag_api')
    list_filter = ('flag_api', 'box')
    # history_list_display = ['name', 'box', 'quantity', 'flag_api']


@admin.register(Unit)
class UnitAdmin(SimpleHistoryAdmin):
    list_display = ('moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start')
    # history_list_display = ['moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start']
    list_filter = ('dexterity', )


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

