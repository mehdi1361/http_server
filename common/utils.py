# -*- encoding: utf-8 -*-
from __future__ import print_function
import random
from objects.models import UserChest, Chest, Unit, Item, UserHero, LeagueUser, CreatedLeague, UserCard, League, Hero
from django.conf import settings
from system_settings.models import CTM, CTMHero
from random import shuffle
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

    def __init__(self, user, chest_type_index=None, chest_type='non_free'):
        self.user = user
        self.chest_type_index = chest_type_index
        self.chest_type = chest_type

    def generate_chest(self):
        cards_type = 4
        lst_unit = []

        if not UserChest.deck_is_open(self.user, self.chest_type):
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

    def generate_tutorial_chest(self):
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
                },
            "chest_monetaryType": "free"
        }

        if self.chest_type_index is None:
            UserChest.objects.create(**data)
            return {"status": True, "message": "chest created"}

        return data["reward_data"]

    def _get_card(self, count, lst_unit):
        # unit_index = random.randint(1, Unit.count())
        unit_list = list(Unit.objects.filter(unlock=True).values_list('id', flat=True))
        unit_index = random.choice(unit_list)
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

    data['max_health'] = data['health']
    data['shield'] = data['shield']
    data['quantity'] = hero_user.quantity if hero_user else 0

    if hero_user.level == 0:
        next_stats = hero_user.level + 2
    else:
        next_stats = hero_user.level + 1

    data['level'] = hero_user.level if hero_user.hero and hero_user else 0

    data['next_upgrade_stats'] = {
        'card_cost': settings.HERO_UPDATE[next_stats]['coins'],

        'card_count': settings.HERO_UPDATE[next_stats]['hero_cards'],

        'attack': int(round(data['attack'] + data['attack'] * settings.HERO_UPDATE[next_stats]['increase'])),

        'health': int(round(data['health'] + data['health'] * settings.HERO_UPDATE[next_stats]['increase'])),

        'shield': int(round(data['shield'] + data['shield'] * settings.HERO_UPDATE[next_stats]['increase'])),

        'critical_chance': data['critical_chance'],

        'critical_ratio': data['critical_ratio'],
        'miss_chance': data['miss_chance'],
        'dodge_chance': data['dodge_chance']
    }

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
            'critical_chance': hero_user.hero.chakra_critical_chance,
            'critical_ratio': hero_user.hero.chakra_critical_ratio,
            'miss_chance': hero_user.hero.chakra_miss_chance,
            'dodge_chance': hero_user.hero.chakra_dodge_chance

        }
    }
    return data


def unit_normalize_data(unit, data):
    if unit.level in settings.UNIT_UPDATE.keys():
        health = int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[unit.level]['increase']))
        shield = int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[unit.level]['increase']))

        if unit.level == 0:
            next_stats = unit.level + 2
        else:
            next_stats = unit.level + 1

        data['next_upgrade_stats'] = {
            'card_cost': settings.UNIT_UPDATE[next_stats]['coins'],
            'card_count': settings.UNIT_UPDATE[next_stats]['unit_cards'],
            'attack': int(round(data['attack'] + data['attack'] * settings.UNIT_UPDATE[next_stats]['increase'])),
            'health': int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[next_stats]['increase'])),
            'shield': int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[next_stats]['increase'])),

            'critical_chance': data['critical_chance'],
            'critical_ratio': data['critical_ratio'],
            'miss_chance': data['miss_chance'],
            'dodge_chance': data['dodge_chance']
        }

        data['health'] = health
        data['max_health'] = health
        data['shield'] = shield
        data['max_shield'] = shield

        data['attack'] = int(
            round(data['attack'] + data['attack'] * settings.UNIT_UPDATE[unit.level]['increase']))

    data['quantity'] = unit.quantity
    data['max_health'] = data['health']
    data['max_shield'] = data['shield']
    data['level'] = unit.level
    data['cool_down'] = unit.is_cool_down
    data['cool_down_remaining_seconds'] = unit.cool_down_remain_time

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


def league_status(player, league):
    promoting_lst = LeagueUser.objects.values_list('player', flat=True).filter(league=league.league).order_by('-score')[
                    :league.league.base_league.promoting_count]
    if player.id in promoting_lst:
        return 'promoting'

    demoting_lst = LeagueUser.objects.values_list('player', flat=True).filter(league=league.league).order_by('score')[
                   :league.league.base_league.demoting_count]

    if player.id in demoting_lst:
        return 'demoting'

    return 'normal'


class CtmChestGenerate:

    def __init__(self, user, chest_type_index=None, chest_type='W', league=None):
        try:
            if league is None:
                league = LeagueUser.objects.get(player=user.user_currency, close_league=False)
                self.league = league.league.base_league

            else:
                self.league = league

        except LeagueUser.DoesNotExist:
            self.league = League.objects.get(league_name='Cooper01')

        self.user = user
        self.chest_type_index = chest_type_index
        self.chest_type = chest_type
        self.selected_hero = False
        self.result = []

    def generate_chest(self):

        if not UserChest.deck_is_open(self.user):
            return {"status": False, "message": "deck is full"}

        if self.chest_type_index is None:
            index, chest_type = UserChest.get_sequence(self.user)
            chest = Chest.get(chest_type)

        else:
            chest = Chest.get(self.chest_type)

        data = {
            "user": self.user,
            "chest": chest,
            "sequence_number": UserChest.next_sequence(self.user),
            "reward_data": self._get_card()
        }

        if self.chest_type_index == 'chest':
            UserChest.objects.create(**data)
            return {"status": True, "message": "chest created"}

        return data["reward_data"]

    def generate_tutorial_chest(self):

        if not UserChest.deck_is_open(self.user):
            return {"status": False, "message": "deck is full"}

        if self.chest_type_index is None:
            index, chest_type = UserChest.get_sequence(self.user)
            chest = Chest.get(chest_type)

        else:
            chest = Chest.get(self.chest_type_index)

        data = {
            "user": self.user,
            "chest": chest,
            "sequence_number": UserChest.next_sequence(self.user),
            "reward_data": self._get_card(is_tutorial=True),
            "chest_monetaryType": "free"
        }

        if self.chest_type_index is None:
            UserChest.objects.create(**data)
            return {"status": True, "message": "chest created"}

        return data["reward_data"]

    def _get_card(self, is_tutorial=False):
        self.result = []
        if is_tutorial:
            ctm = CTM.objects.get(params__is_tutorial='True')

        else:
            ctm = CTM.objects.get(league=self.league, chest_type=self.chest_type)

        lst_result = []
        hero_result = None
        lst_exclude = []
        lst_hero_name = list(Hero.objects.all().values_list('moniker', flat=True))

        for i in range(0, ctm.card_try):
            if not self.selected_hero:
                lst_valid_hero = []
                for hero in ctm.heroes.filter(enable=True):
                    lst_valid_hero.append(hero.hero.id)

                random_hero_chance = random.uniform(1, 100)

                if ctm.chance_hero >= random_hero_chance:
                    user_heroes = list(UserHero.objects.filter(user=self.user, hero_id__in=lst_valid_hero))
                    if user_heroes is not None:
                        random_user_hero = user_heroes[random.randint(0, len(user_heroes) - 1)]

                        if random_user_hero.quantity > settings.HERO_UPDATE[random_user_hero.level + 1]['hero_cards']:
                            valid_card = random_user_hero.quantity \
                                         - settings.HERO_UPDATE[random_user_hero.level + 1]['hero_cards']
                        else:
                            valid_card = settings.HERO_UPDATE[random_user_hero.level + 1][
                                             'hero_cards'] - random_user_hero.quantity

                        variance = 100 + valid_card - random_user_hero.used_count

                        if variance < 20:
                            variance = 20

                        if ctm.chance_hero != 100:
                            lst_result.extend(
                                [{
                                    "name": random_user_hero.hero.moniker,
                                    "type": "hero"
                                }] * variance
                            )

                        hero_result = random_user_hero.hero

                        self.selected_hero = True

            if is_tutorial:
                lst_valid_unit = Unit.valid_units_id(ctm.league)
                for unit in ctm.units.filter(enable=True):
                    lst_valid_unit.append(unit.unit.id)

            else:
                lst_valid_unit = Unit.valid_units_id(ctm.league)

            user_units = list(
                UserCard.objects.filter(user=self.user, character_id__in=lst_valid_unit)
                    .exclude(character_id__in=lst_exclude)
            )

            if user_units is not None:
                random_user_unit = user_units[random.randint(0, len(user_units) - 1)]

                if random_user_unit.quantity > settings.UNIT_UPDATE[random_user_unit.level + 1]['unit_cards']:
                    valid_card = random_user_unit.quantity - \
                                 settings.UNIT_UPDATE[random_user_unit.level + 1]['unit_cards']
                else:
                    valid_card = settings.UNIT_UPDATE[random_user_unit.level + 1]['unit_cards'] \
                                 - random_user_unit.quantity

                variance = 100 + valid_card - random_user_unit.used_quantity

                if variance < 20:
                    variance = 20

                lst_result.extend(
                    [{
                        "name": random_user_unit.character.moniker,
                        "type": "troop"
                    }] * variance
                )

                lst_exclude.append(random_user_unit.character.id)

        shuffle(lst_result)
        tmp_lst = []

        sum_card = 0
        while len(self.result) < ctm.card_try:
            if ctm.chance_hero == 100 and hero_result.moniker not in tmp_lst:
                self.result.append(
                    {
                        "unit": str(hero_result.moniker),
                        "count": random.randint(ctm.min_hero, ctm.max_hero)
                    }
                )

                tmp_lst.append(hero_result.moniker)

            lst_result = [k for k in lst_result if k['name'] not in tmp_lst]
            idx = random.randint(0, len(lst_result) - 1)

            if lst_result[idx]['name'] not in tmp_lst:
                candid_num = random.randint(ctm.min_troop, int(ctm.total / ctm.card_try)) \
                    if lst_result[idx]['type'] == 'troop' \
                    else random.randint(ctm.min_hero, int(ctm.total / ctm.card_try))

                sum_card += candid_num
                self.result.append(
                    {
                        "unit": str(lst_result[idx]['name']),
                        "count": candid_num
                    }
                )

                tmp_lst.append(lst_result[idx]['name'])

        while sum_card < ctm.total:
            rd_idx = random.randint(0, len(self.result) - 1)
            diff_val = ctm.total - sum_card

            if diff_val > 0:
                rnd_max = diff_val / ctm.card_try if int(diff_val / ctm.card_try) > 0 else 1
                rand_val = random.randint(1, rnd_max)

                if self.result[rd_idx]['unit'] not in lst_hero_name:
                    self.result[rd_idx]['count'] += rand_val
                    sum_card += rand_val

        data = {
            "chest_type": ctm.get_chest_type_display(),
            "gems": random.randint(ctm.min_gem, ctm.max_gem),
            "coins": random.randint(ctm.min_coin, ctm.max_coin),
            "units": self.result,
            "reward_range": {
                "type": ctm.get_chest_type_display(),
                "min_coin": ctm.min_coin,
                "max_coin": ctm.max_coin,
                "min_gem": ctm.min_gem,
                "max_gem": ctm.max_gem,
                "card_count": ctm.total,
                "min_hero": ctm.min_hero,
                "max_hero": ctm.max_hero,
                "hero_card_chance": ctm.chance_hero
            }
        }

        return data
