from __future__ import print_function
import random
from objects.models import UserChest, Chest, Unit, Item, UserHero
from django.conf import settings


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


class ChestGenerate:

    def __init__(self, user, chest_type_index=None):
        self.user = user
        self.chest_type_index = chest_type_index

    def generate_chest(self):
        cards_type = 4
        lst_unit = []

        if not UserChest.deck_is_open(self.user, 'non_free'):
            return {"status": False, "message": "deck is full"}

        if self.chest_type_index is None:
            index, chest_type = UserChest.get_sequence(self.user)
            chest = Chest.get(chest_type)

        else:
            chest = Chest.get(self.chest_type_index)

        max_unit_card_count = chest.unit_card

        if chest.hero_card > 0:
            cards_type -= 1
            # TODO create hero card

        for i in range(0, cards_type):
            if i != cards_type:
                count = random.randint(1, max_unit_card_count)

            else:
                count = max_unit_card_count

            lst_unit = self._get_card(count, lst_unit)

            max_unit_card_count -= count
            if max_unit_card_count <= 0:
                break

        data = {
            "user": self.user,
            "chest": chest,
            "sequence_number": UserChest.next_sequence(self.user),
            "reward_data":
                {
                    "chest_type": chest.get_chest_type_display(),
                    "gems": random.randint(chest.min_gem, chest.max_gem),
                    "coins": random.randint(chest.min_coin, chest.max_coin),
                    "units": lst_unit
                }
        }

        if self.chest_type_index is None:
            UserChest.objects.create(**data)
            return {"status": True, "message": "chest created"}

        return data["reward_data"]

    def _get_card(self, count, lst_unit):
        unit_index = random.randint(1, Unit.count())
        unit = Unit.objects.get(pk=unit_index)

        data = {
            "unit": str(unit),
            "count": count
        }

        find_match = False

        for item in lst_unit:
            if item["unit"] == unit:
                find_match = True
                item["count"] += count

        if not find_match:
            lst_unit.append(data)

        return lst_unit


def hero_normalize_data(hero_user, data):
    data['selected_hero'] = True if hero_user.enable_hero else False
    if hero_user.level in settings.HERO_UPDATE.keys():
        health = int(round(data['health'] + data['health'] * settings.HERO_UPDATE[hero_user.level]['increase']))
        shield = int(round(data['shield'] + data['shield'] * settings.HERO_UPDATE[hero_user.level]['increase']))
        data['health'] = health
        data['max_health'] = health
        data['shield'] = shield
        data['max_shield'] = shield
        data['attack'] = data['attack'] + data['attack'] * settings.HERO_UPDATE[hero_user.level]['increase']
        data['critical_chance'] = round(
            data['critical_chance'] + data['critical_chance'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)
        data['critical_ratio'] = round(
            data['critical_ratio'] + data['critical_ratio'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)
        data['miss_chance'] = round(
            data['miss_chance'] + data['miss_chance'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)
        data['dodge_chance'] = round(
            data['dodge_chance'] + data['dodge_chance'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)

    data['max_health'] = data['health']
    data['shield'] = data['shield']
    data['quantity'] = hero_user.quantity if hero_user else 0

    data['next_upgrade_stats'] = {
        'card_cost': settings.HERO_UPDATE[hero_user.level + 1]['coins'],

        'card_count': settings.HERO_UPDATE[hero_user.level + 1]['hero_cards'],

        'attack': int(round(data['attack'] + data['attack'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),

        'health': int(round(data['health'] + data['health'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),

        'shield': int(round(data['shield'] + data['shield'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),

        'critical_chance': round(
            data['critical_chance'] + data['critical_chance'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'],
            2),

        'critical_ratio': round(
            data['critical_ratio'] + data['critical_ratio'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),

        'miss_chance': round(
            data['miss_chance'] + data['miss_chance'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),

        'dodge_chance': round(
            data['dodge_chance'] + data['dodge_chance'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2)

    }

    data['level'] = hero_user.level if hero_user.hero and hero_user else 0

    data['chakra'] = {
        'chakra_moniker': hero_user.hero.chakra_moniker,
        'chakra_health': hero_user.hero.chakra_health,
        'chakra_shield': hero_user.hero.chakra_shield,
        'chakra_attack': hero_user.hero.chakra_attack,
        'chakra_critical_chance': hero_user.hero.chakra_critical_chance,
        'chakra_critical_ratio': hero_user.hero.chakra_critical_ratio,
        'chakra_miss_chance': hero_user.hero.chakra_miss_chance,
        'chakra_dodge_chance': hero_user.hero.chakra_dodge_chance,
        'chakra_max_health': hero_user.hero.chakra_max_health,
        'chakra_max_shield': hero_user.hero.chakra_max_shield,
        'next_upgrade_stats': {
            'attack': int(round(
                hero_user.hero.chakra_attack + hero_user.hero.chakra_attack * settings.HERO_UPDATE[hero_user.level + 1][
                    'increase'])),
            'health': int(round(
                hero_user.hero.chakra_health + hero_user.hero.chakra_health * settings.HERO_UPDATE[hero_user.level + 1][
                    'increase'])),
            'shield': int(round(
                hero_user.hero.chakra_shield + hero_user.hero.chakra_shield * settings.HERO_UPDATE[hero_user.level + 1][
                    'increase'])),
            'critical_chance': round(hero_user.hero.chakra_critical_chance + hero_user.hero.chakra_critical_chance *
                                     settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),
            'critical_ratio': round(hero_user.hero.chakra_critical_ratio + hero_user.hero.chakra_critical_ratio *
                                    settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),
            'miss_chance': round(hero_user.hero.chakra_miss_chance + hero_user.hero.chakra_miss_chance *
                                 settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),
            'dodge_chance': round(hero_user.hero.chakra_dodge_chance + hero_user.hero.chakra_dodge_chance *
                                  settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2)

        }
    }
    return data


def unit_normalize_data(unit, data):
    if unit.level in settings.UNIT_UPDATE.keys():
        health = int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[unit.level]['increase']))
        shield = int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[unit.level]['increase']))

        data['health'] = health
        data['max_health'] = health
        data['shield'] = shield
        data['max_shield'] = shield

        data['attack'] = int(
            round(data['attack'] + data['attack'] * settings.UNIT_UPDATE[unit.level]['increase']))
        data['critical_chance'] = round(
            data['critical_chance'] + data['critical_chance'] * settings.UNIT_UPDATE[unit.level]['increase'])

        data['critical_ratio'] = round(
            data['critical_ratio'] + data['critical_ratio'] * settings.UNIT_UPDATE[unit.level]['increase'])

        data['miss_chance'] = round(
            data['miss_chance'] + data['miss_chance'] * settings.UNIT_UPDATE[unit.level]['increase'])

        data['dodge_chance'] = round(
            data['dodge_chance'] + data['dodge_chance'] * settings.UNIT_UPDATE[unit.level]['increase'])

    data['quantity'] = unit.quantity
    data['max_health'] = data['health']
    data['max_shield'] = data['shield']

    data['next_upgrade_stats'] = {
        'card_cost': settings.UNIT_UPDATE[unit.level + 1]['coins'],
        'card_count': settings.UNIT_UPDATE[unit.level + 1]['unit_cards'],
        'attack': int(round(data['attack'] + data['attack'] * settings.UNIT_UPDATE[unit.level + 1]['increase'])),
        'health': int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[unit.level + 1]['increase'])),
        'shield': int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[unit.level + 1]['increase'])),
        'critical_chance': round(data['critical_chance'] + data['critical_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2),
        'critical_ratio': round(data['critical_ratio'] + data['critical_ratio'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2),
        'miss_chance': round(data['miss_chance'] + data['miss_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2),
        'dodge_chance': round(data['dodge_chance'] + data['dodge_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2)
    }

    data['level'] = unit.level
    data['cool_down'] = unit.is_cool_down
    data['cool_down_remaining_seconds'] = 0

    return data


def item_normalize_data(item, data):
    data['next_upgrade_stats'] = {
        'card_cost': settings.ITEM_UPDATE[item.level + 1]['coins'],
        'card_count': settings.ITEM_UPDATE[item.level + 1]['item_cards'],
        'damage': int(round(
            data['damage'] + data['damage'] * settings.ITEM_UPDATE[item.level + 1]['increase'])),
        'health': int(round(
            data['health'] + data['health'] * settings.ITEM_UPDATE[item.level + 1]['increase'])),
        'shield': int(round(
            data['shield'] + data['shield'] * settings.ITEM_UPDATE[item.level + 1]['increase'])),
        'critical_chance': round(data['critical_chance'] + data['critical_chance'] *
                                 settings.ITEM_UPDATE[item.level + 1]['increase']),
        'critical_ratio': round(data['critical_ratio'] + data['critical_ratio'] *
                                settings.ITEM_UPDATE[item.level + 1]['increase'])
    }

    data['quantity'] = item.quantity
    data['next_upgrade_card_cost'] = settings.ITEM_UPDATE[item.level + 1]['coins']
    data['next_upgrade_card_count'] = settings.ITEM_UPDATE[item.level + 1]['item_cards']
    data['level'] = item.level

    return data