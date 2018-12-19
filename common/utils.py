# -*- encoding: utf-8 -*-
from __future__ import print_function
import random
from objects.models import UserChest, Chest, Unit, Item, UserHero, \
    LeagueUser, CreatedLeague, UserCard, League, Hero, UnitSpell, HeroSpell, ChakraSpell
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
    lst_stat = []

    if hero_user.level == 0:
        next_stats = hero_user.level + 2
    else:
        next_stats = hero_user.level + 1

    health = int(round(data['health'] + data['health'] * settings.HERO_UPDATE[hero_user.level]['increase']))
    shield = int(round(data['shield'] + data['shield'] * settings.HERO_UPDATE[hero_user.level]['increase']))

    if hero_user.level in settings.HERO_UPDATE.keys():
        for key in ['attack', 'health',
                    'shield', 'critical_chance',
                    'critical_ratio', 'miss_chance', 'dodge_chance'
                    ]:
            if key in ['attack', 'health', 'shield']:
                val = int(round(data[key] + data[key] * settings.HERO_UPDATE[hero_user.level]['increase']))
                nval = int(round(data[key] + data[key] * settings.HERO_UPDATE[next_stats]['increase']))

            else:
                val = data[key]
                nval = data[key]

            lst_stat.append(
                {
                    "name": key,
                    "val": val,
                    "nval": nval
                }
            )

            if key in ['health', 'shield']:
                lst_stat.append(
                    {
                        "name": "max_{}".format(key),
                        "val": val,
                        "nval": nval
                    }
                )

            data.pop(key, None)

    data['lst_stat'] = lst_stat
    data['max_health'] = health
    data['max_shield'] = shield
    data['quantity'] = hero_user.quantity if hero_user else 0

    data['level'] = hero_user.level if hero_user.hero and hero_user else 0
    data['next_card_count'] = settings.HERO_UPDATE[next_stats]['hero_cards']
    data['card_cost'] = settings.HERO_UPDATE[next_stats]['coins']

    data['chakra'] = {
        'chakra_moniker': hero_user.hero.chakra_moniker,
        'lst_stat': [
            {
                "name": "health",
                "val": hero_user.hero.chakra_health,
                "nval": int(
                    round(hero_user.hero.chakra_health + hero_user.hero.chakra_health *
                          settings.HERO_UPDATE[hero_user.level + 1]['increase'])
                )
            },
            {
                "name": "shield",
                "val": hero_user.hero.chakra_shield,
                "nval": int(
                    round(hero_user.hero.chakra_shield + hero_user.hero.chakra_shield *
                          settings.HERO_UPDATE[hero_user.level + 1]['increase'])
                )
            },
            {
                "name": "max_health",
                "val": hero_user.hero.chakra_health,
                "nval": int(
                    round(hero_user.hero.chakra_health + hero_user.hero.chakra_health *
                          settings.HERO_UPDATE[hero_user.level + 1]['increase'])
                )
            },
            {
                "name": "max_shield",
                "val": hero_user.hero.chakra_shield,
                "nval": int(
                    round(hero_user.hero.chakra_shield + hero_user.hero.chakra_shield *
                          settings.HERO_UPDATE[hero_user.level + 1]['increase'])
                )
            },
            {
                "name": "attack",
                "val": hero_user.hero.chakra_attack,
                "nval": int(
                    round(hero_user.hero.chakra_attack + hero_user.hero.chakra_attack *
                          settings.HERO_UPDATE[hero_user.level + 1]['increase'])
                )
            },
            {
                "name": "critical_chance",
                "val": hero_user.hero.chakra_critical_chance,
                "nval": hero_user.hero.chakra_critical_chance
            },
            {
                "name": "critical_ratio",
                "val": hero_user.hero.chakra_critical_ratio,
                "nval": hero_user.hero.chakra_critical_ratio
            },
            {
                "name": "critical_ratio",
                "val": hero_user.hero.chakra_critical_ratio,
                "nval": hero_user.hero.chakra_critical_ratio
            },
            {
                "name": "critical_chance",
                "val": hero_user.hero.chakra_miss_chance,
                "nval": hero_user.hero.chakra_miss_chance
            },
            {
                "name": "miss_chance",
                "val": hero_user.hero.chakra_miss_chance,
                "nval": hero_user.hero.chakra_miss_chance
            },
            {
                "name": "dodge_chance",
                "val": hero_user.hero.chakra_dodge_chance,
                "nval": hero_user.hero.chakra_dodge_chance
            }
        ]
    }

    return data


def unit_normalize_data(unit, data):
    lst_stat = []
    if unit.level in settings.UNIT_UPDATE.keys():
        health = int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[unit.level]['increase']))
        shield = int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[unit.level]['increase']))

        if unit.level == 0:
            next_stats = unit.level + 2
        else:
            next_stats = unit.level + 1

        for key in ['attack', 'health',
                    'shield', 'critical_chance',
                    'critical_ratio', 'miss_chance', 'dodge_chance'
                    ]:
            if key in ['attack', 'health', 'shield']:
                val = int(round(data[key] + data[key] * settings.UNIT_UPDATE[unit.level]['increase']))
                nval = int(round(data[key] + data[key] * settings.UNIT_UPDATE[next_stats]['increase']))

            else:
                val = data[key]
                nval = data[key]

            lst_stat.append(
                {
                    "name": key,
                    "val": val,
                    "nval": nval
                }
            )

            if key in ['health', 'shield']:
                lst_stat.append(
                    {
                        "name": "max_{}".format(key),
                        "val": val,
                        "nval": nval
                    }
                )

            data.pop(key, None)

        data['lst_stat'] = lst_stat

        data['max_health'] = health
        data['max_shield'] = shield
        data['next_card_count'] = settings.UNIT_UPDATE[next_stats]['unit_cards']
        data['next_card_cost'] = settings.UNIT_UPDATE[next_stats]['coins']

    data['quantity'] = unit.quantity
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


class MCtmChestGenerate:

    def __init__(self, user, chest_type_index=None, chest_type='W', league=None):
        try:
            if league is None:
                league = LeagueUser.objects.get(player=user.user_currency, close_league=False)
                self.league = league.league.base_league

            else:
                self.league = league

        except LeagueUser.DoesNotExist:
            self.league = League.objects.get(league_name='Cooper00')

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

    def __get_card(self, is_tutorial=False):
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
                UserCard.objects.filter(user=self.user, character_id__in=lst_valid_unit).exclude
                (character_id__in=lst_exclude)
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

    def _get_card(self, is_tutorial=False):
        if is_tutorial:
            ctm = CTM.objects.get(params__is_tutorial='True')

        else:
            ctm = CTM.objects.get(league=self.league, chest_type=self.chest_type)

        for i in range(0, ctm.card_try):
            pass

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


class CtmChestGenerate(object):

    def __init__(self, user, chest_type_index=None, chest_type='W', league=None, is_tutorial=None):
        try:
            if league is None:
                league = LeagueUser.objects.get(player=user.user_currency, close_league=False)
                self.league = league.league.base_league

            else:
                self.league = league

        except LeagueUser.DoesNotExist:
            self.league = League.objects.get(league_name='Cooper00')

        finally:
            self.user = user
            self.chest_type_index = chest_type_index
            self.chest_type = chest_type
            self.selected_hero = False
            self.result = []
            self.is_tutorial = is_tutorial

            if self.is_tutorial:
                self.ctm = CTM.objects.get(params__is_tutorial='True')
            else:
                self.ctm = CTM.objects.get(league=self.league, chest_type=self.chest_type)

            self.lst_hero_name = list(Hero.objects.all().values_list('moniker', flat=True))
            self.sum_card = 0

    def _calc_data(foo):

        def magic(self, *args, **kwargs):
            self.__reset()
            self.__must_have()
            while len(self.result) < self.ctm.card_try:
                self.__epic()
                self.__rare()
                self.__common()

            self.__normal()

            return foo(self, *args, **kwargs)

        return magic

    def __reset(self):
        self.result = []
        self.sum_card = 0

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
            "reward_data": self.get_card()
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

    def __must_have(self):
        if self.ctm.is_must_have_hero:

            if self.ctm.must_have_hero_type == 'random':
                count_hero = self.ctm.must_have_hero.count()

                if count_hero < 1:
                    raise Exception("no hero choice")

                rand_index = random.randint(0, count_hero - 1)
                random_hero = self.ctm.must_have_hero.all()[rand_index]

                count_card = random.randint(self.ctm.min_have_hero, self.ctm.max_have_hero)
                self.result.append({
                    "name": str(random_hero),
                    "type": "hero",
                    "rarity": "epic",
                    "count": count_card
                })

                self.sum_card += count_card

            else:
                for hero in self.ctm.must_have_hero.all():
                    count_card = random.randint(self.ctm.min_have_hero, self.ctm.max_have_hero)
                    self.result.append({
                        "name": str(hero),
                        "type": "hero",
                        "rarity": "epic",
                        "count": count_card
                    })

                    self.sum_card += count_card

        if self.ctm.is_must_have_spell:
            if self.ctm.must_have_spell_type == 'random':

                count_spell = self.ctm.must_have_spell.count()
                if count_spell < 1:
                    raise Exception("no spell choice")

                rand_index = random.randint(0, count_spell - 1)
                random_spell = self.ctm.must_have_spell.all()[rand_index]
                count_card = random.randint(self.ctm.min_have_spell, self.ctm.max_have_spell)
                self.result.append({
                    "name": str(random_spell),
                    "type": "spell",
                    "rarity": random_spell.rarity,
                    "count": count_card
                })

                self.sum_card += count_card

            else:
                for spell in self.ctm.must_have_spell.all():
                    count_card = random.randint(self.ctm.min_have_spell, self.ctm.max_have_spell)
                    self.result.append({
                        "name": str(spell),
                        "type": "spell",
                        "rarity": spell.rarity,
                        "count": count_card
                    })

                    self.sum_card += count_card

        if self.ctm.is_must_have_troop:
            if self.ctm.must_have_troop_type == 'random':

                count_troop = self.ctm.must_have_troop.count()
                if count_troop < 1:
                    raise Exception("no troop choice")

                rand_index = random.randint(0, count_troop - 1)
                random_troop = self.ctm.must_have_troop.all()[rand_index]
                count_card = random.randint(self.ctm.min_have_troop, self.ctm.max_have_troop)

                self.result.append({
                    "name": str(random_troop),
                    "type": "troop",
                    "rarity": random_troop.rarity,
                    "count": count_card
                })

                self.sum_card += count_card

            else:
                count_card = random.randint(self.ctm.min_have_troop, self.ctm.max_have_troop)
                for troop in self.ctm.must_have_troop.all():
                    self.result.append({
                        "name": str(troop),
                        "type": "troop",
                        "rarity": troop.rarity,
                        "count": count_card
                    })

                    self.sum_card += count_card

    def __normal(self):
        while self.sum_card < self.ctm.total:
            rd_idx = random.randint(0, len(self.result) - 1)
            diff_val = self.ctm.total - self.sum_card

            if diff_val > 0:
                rnd_max = diff_val / self.ctm.card_try if int(diff_val / self.ctm.card_try) > 0 else 1
                rand_val = random.randint(1, rnd_max)

                if self.result[rd_idx]['name'] not in self.lst_hero_name:
                    self.result[rd_idx]['count'] += rand_val
                    self.sum_card += rand_val

    def __epic(self):

        lst_epic_card = []
        epic_chance = random.randint(0, 100)

        if self.ctm.epic_chance > epic_chance:
            '''add hero card in epic chance'''
            for user_hero in self.user.user_hero.all():
                if user_hero.quantity > settings.HERO_UPDATE[user_hero.level + 1]['hero_cards']:
                    valid_card = user_hero.quantity - settings.HERO_UPDATE[user_hero.level + 1]['hero_cards']

                else:
                    valid_card = settings.HERO_UPDATE[user_hero.level + 1]['hero_cards'] - user_hero.quantity

                lst_epic_card.extend([{
                    "name": user_hero.hero.moniker,
                    "type": "hero",
                    "rarity": "epic"
                }] * (100 + valid_card - user_hero.used_count)
                                     )

            '''add unit card in epic chance'''
            for user_card in self.user.cards.filter(character__unlock=True, character__rarity='epic'):
                if user_card.quantity > settings.UNIT_UPDATE[user_card.level + 1]['unit_cards']:
                    valid_card = user_card.quantity - \
                                 settings.UNIT_UPDATE[user_card.level + 1]['unit_cards']
                else:
                    valid_card = settings.UNIT_UPDATE[user_card.level + 1]['unit_cards'] \
                                 - user_card.quantity

                lst_epic_card.extend([{
                    "name": str(user_card.character),
                    "type": "unit",
                    "rarity": "epic"
                }] * (100 + valid_card - user_card.used_quantity)
                                     )

            for spell in UnitSpell.objects.filter(rarity='epic'):
                lst_epic_card.extend(
                    [{
                        "name": str(spell),
                        "type": "unit_spell",
                        "rarity": "epic"
                    }] * 100
                )

            for spell in HeroSpell.objects.filter(rarity='epic'):
                lst_epic_card.extend(
                    [{
                        "name": str(spell),
                        "type": "hero_spell",
                        "rarity": "epic"
                    }] * 100
                )

            for spell in ChakraSpell.objects.filter(rarity='epic'):
                lst_epic_card.extend(
                    [{
                        "name": str(spell),
                        "type": "chakra_spell",
                        "rarity": "epic"
                    }] * 100
                )

            if len(lst_epic_card) > 0:
                random_idx = random.randint(0, len(lst_epic_card) - 1)
                shuffle(lst_epic_card)
                epic_result = lst_epic_card[random_idx]

                count_card = random.randint(self.ctm.min_epic, self.ctm.max_epic)
                epic_result['count'] = count_card
                self.sum_card += count_card

                self.result.append(epic_result)

    def __rare(self):

        # add unit card in epic chance

        lst_rare_card = []

        for user_card in self.user.cards.filter(character__unlock=True, character__rarity='rare'):
            if user_card.quantity > settings.UNIT_UPDATE[user_card.level + 1]['unit_cards']:
                valid_card = user_card.quantity - \
                             settings.UNIT_UPDATE[user_card.level + 1]['unit_cards']
            else:
                valid_card = settings.UNIT_UPDATE[user_card.level + 1]['unit_cards'] \
                             - user_card.quantity

            lst_rare_card.extend(
                [{
                    "name": str(user_card.character),
                    "type": "unit",
                    "rarity": "rare"
                }] * (100 + valid_card - user_card.used_quantity)
            )

        for spell in UnitSpell.objects.filter(rarity='rare'):
            lst_rare_card.extend(
                [{
                    "name": str(spell),
                    "type": "unit_spell",
                    "rarity": "rare"
                }] * 100
            )

        for spell in HeroSpell.objects.filter(rarity='rare'):
            lst_rare_card.extend(
                [{
                    "name": str(spell),
                    "type": "hero_spell",
                    "rarity": "rare"
                }] * 100
            )

        for spell in ChakraSpell.objects.filter(rarity='rare'):
            lst_rare_card.extend(
                [{
                    "name": str(spell),
                    "type": "chakra_spell",
                    "rarity": "rare"
                }] * 100
            )

        if len(lst_rare_card) > 0:
            random_idx = random.randint(0, len(lst_rare_card) - 1)
            shuffle(lst_rare_card)
            rare_result = lst_rare_card[random_idx]

            count_card = random.randint(self.ctm.min_epic, self.ctm.max_epic)
            rare_result['count'] = count_card
            self.sum_card += count_card

            self.result.append(rare_result)

    def __common(self):

        # add unit card in epic chance

        lst_common_card = []

        for user_card in self.user.cards.filter(character__unlock=True, character__rarity='common'):
            if user_card.quantity > settings.UNIT_UPDATE[user_card.level + 1]['unit_cards']:
                valid_card = user_card.quantity - \
                             settings.UNIT_UPDATE[user_card.level + 1]['unit_cards']
            else:
                valid_card = settings.UNIT_UPDATE[user_card.level + 1]['unit_cards'] \
                             - user_card.quantity

            lst_common_card.extend(
                [{
                    "name": str(user_card.character),
                    "type": "unit",
                    "rarity": "common"
                }] * (100 + valid_card - user_card.used_quantity)
            )

        for spell in UnitSpell.objects.filter(rarity='common'):
            lst_common_card.extend(
                [{
                    "name": str(spell),
                    "type": "unit_spell",
                    "rarity": "common"
                }] * 100
            )

        for spell in HeroSpell.objects.filter(rarity='common'):
            lst_common_card.extend(
                [{
                    "name": str(spell),
                    "type": "hero_spell",
                    "rarity": "common"
                }] * 100
            )

        for spell in ChakraSpell.objects.filter(rarity='common'):
            lst_common_card.extend(
                [{
                    "name": str(spell),
                    "type": "chakra_spell",
                    "rarity": "common"
                }] * 100
            )

        if len(lst_common_card) > 0:
            random_idx = random.randint(0, len(lst_common_card) - 1)
            shuffle(lst_common_card)
            common_result = lst_common_card[random_idx]

            count_card = random.randint(self.ctm.min_epic, self.ctm.max_epic)
            common_result['count'] = count_card

            self.sum_card += count_card
            self.result.append(common_result)

    @_calc_data
    def get_card(self):
        return {
            "chest_type": self.ctm.get_chest_type_display(),
            "gems": random.randint(self.ctm.min_gem, self.ctm.max_gem),
            "coins": random.randint(self.ctm.min_coin, self.ctm.max_coin),
            "units": self.result,
            "reward_range": {
                "type": self.ctm.get_chest_type_display(),
                "min_coin": self.ctm.min_coin,
                "max_coin": self.ctm.max_coin,
                "min_gem": self.ctm.min_gem,
                "max_gem": self.ctm.max_gem,
                "card_count": self.ctm.total  # ,
                # "min_hero": ctm.min_hero,
                # "max_hero": ctm.max_hero,
                # "hero_card_chance": ctm.chance_hero
            }
        }
