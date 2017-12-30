# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import BenefitBox, Unit, Hero, HeroUnits,
# from django.contrib.auth.models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name')
#     list_filter = ('is_staff', 'is_superuser')


class HeroUnits(admin.StackedInline):
    model = HeroUnits


@admin.register(BenefitBox)
class BenefitBoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'box', 'quantity', 'flag_api')
    list_filter = ('flag_api', 'box')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start')
    list_filter = ('dexterity', )


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('moniker', 'health', 'shield', 'attack', 'dexterity', 'enable_in_start')
    list_filter = ('dexterity', )
    inlines = [HeroUnits]

