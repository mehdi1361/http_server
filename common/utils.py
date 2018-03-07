from __future__ import print_function
import random
from objects.models import UserChest, Chest, Unit, Item


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
            "cards":
                {
                    "gems": random.randint(chest.min_gem, chest.max_gem),
                    "coins": random.randint(chest.min_coin, chest.max_coin),
                    "units": lst_unit
                }
        }

        if self.chest_type_index is None:
            UserChest.objects.create(**data)
            return {"status": True, "message": "chest created"}

        return data["cards"]

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
