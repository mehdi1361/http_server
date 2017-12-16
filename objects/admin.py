# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import BenefitBox, Unit, Hero


@admin.register(BenefitBox)
class BenefitBoxAdmin(admin.ModelAdmin):
    model = BenefitBox
    list_display = ('name', 'box', 'quantity', 'flag_api')
    list_filter = ('flag_api', 'box')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    model = Unit
    list_display = ('name', 'health', 'shield', 'attack', 'dexterity')
    list_filter = ('dexterity', )


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    model = Hero
    list_display = ('name', 'health', 'shield', 'attack', 'dexterity')
    list_filter = ('dexterity', )
