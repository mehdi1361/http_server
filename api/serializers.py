from django.contrib.auth import get_user_model
from rest_framework import serializers
from objects.models import BenefitBox, UserCurrency, Hero, Unit, UserHero, HeroUnits, UserCard, \
    LeagueInfo, Chest, UserChest, Item, UserItem
from shopping.models import Shop
from message.models import NewsLetter, Inbox
from django.conf import settings


class NewsLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = (
            'id',
            'subject',
            'body',
            'created_date',
            'updated_date',
            'expire_date'
        )


class UserChestSerializer(serializers.ModelSerializer):
    chest_type = serializers.SerializerMethodField()

    class Meta:
        model = UserChest
        fields = (
            'id',
            'chest_type',
            'chest_monetaryType',
            'skip_gem',
            'remain_time',
            'initial_time',
            'status',
            'reward_data'
        )

    def get_chest_type(self, obj):
        return obj.chest.get_chest_type_display()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'damage',
            'shield',
            'health',
            'critical_ratio',
            'critical_chance',
            'dodge_chance',
            'item_type',
            'default_item'
        )


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = ('name', 'quantity')

    def get_name(self, requests):
        return self.character.id


class UserCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCurrency
        fields = (
            'name',
            'gem',
            'coin',
            'trophy',
            'session_count',
            'need_comeback',
            'can_change_name',
            'next_session_remaining_seconds'
        )


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = (
            'id',
            'moniker',
            'dexterity',
            'attack_type',
            'attack',
            'critical_chance',
            'critical_ratio',
            'miss_chance',
            'dodge_chance',
            'enable_in_start',
            'health',
            'max_health',
            'shield',
            'max_shield'
        )


class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = (
            'id',
            'moniker',
            'dexterity',
            'attack_type',
            'health',
            'shield',
            'attack',
            'critical_chance',
            'critical_ratio',
            'miss_chance',
            'dodge_chance',
            'enable_in_start',
            'max_health',
            'max_shield'
        )


class UserCardSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'character',
            'quantity',
            'level',
            'cool_down',
            'cool_down_remaining_seconds'
        )


class UserHeroSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'user',
            'hero',
            'enable_hero',
            'quantity',
            'level',
            'selected_item'
        )


class UserSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField()
    heroes = serializers.SerializerMethodField()
    general_units = serializers.SerializerMethodField()
    chest = serializers.SerializerMethodField()
    newsletter = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'email',
            'info',
            'heroes',
            'general_units',
            'chest',
            'newsletter'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'currency': {'read_only': True},
            'heroes': {'read_only': True},
            'general_units': {'read_only': True}
        }

    def get_chest(self, requests):
        user_deck = UserChest.deck.filter(user=requests)
        serializer = UserChestSerializer(user_deck, many=True)
        return serializer.data

    def get_info(self, requests):
        try:
            currency = UserCurrency.objects.get(user=requests)
            serializer = UserCurrencySerializer(currency)
            return serializer.data

        except UserCurrency.DoesNotExist as e:
            return None

    def get_heroes(self, requests):
        list_serialize = []
        for hero_user in UserHero.objects.filter(user=requests):
            serializer = HeroSerializer(hero_user.hero)
            data = serializer.data

            data['selected_hero'] = True if hero_user.enable_hero else False
            if hero_user.level in settings.HERO_UPDATE.keys():
                data['health'] = int(round(data['health'] + data['health'] * settings.HERO_UPDATE[hero_user.level]['increase']))
                data['shield'] = int(round(data['shield'] + data['shield'] * settings.HERO_UPDATE[hero_user.level]['increase']))
                data['attack'] = data['attack'] + data['attack'] * settings.HERO_UPDATE[hero_user.level]['increase']
                data['critical_chance'] = round(data['critical_chance'] + data['critical_chance'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)
                data['critical_ratio'] = round(data['critical_ratio'] + data['critical_ratio'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)
                data['miss_chance'] = round(data['miss_chance'] + data['miss_chance'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)
                data['dodge_chance'] = round(data['dodge_chance'] + data['dodge_chance'] * settings.HERO_UPDATE[hero_user.level]['increase'], 2)

            data['quantity'] = hero_user.quantity if hero_user else 0

            data['next_upgrade_stats'] = {
                'card_cost': settings.HERO_UPDATE[hero_user.level + 1]['coins'],

                'card_count': settings.HERO_UPDATE[hero_user.level + 1]['hero_cards'],

                'attack': int(round(data['attack'] + data['attack'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),

                'health': int(round(data['health'] + data['health'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),

                'shield': int(round(data['shield'] + data['shield'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),

                'critical_chance': round(data['critical_chance'] + data['critical_chance'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),

                'critical_ratio': round(data['critical_ratio'] + data['critical_ratio'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),

                'miss_chance': round(data['miss_chance'] + data['miss_chance'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),

                'dodge_chance': round(data['dodge_chance'] + data['dodge_chance'] * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2)


            }

            data['level'] = hero_user.level if hero_user.hero and hero_user else 0

            list_unit = []
            for unit in UserCard.objects.filter(character__heroes=hero_user.hero, user=requests):
                unit_serializer = UnitSerializer(unit.character)
                unit_data = unit_serializer.data

                if unit.level in settings.UNIT_UPDATE.keys():
                    unit_data['health'] = int(round(unit_data['health'] + unit_data['health'] *settings.UNIT_UPDATE[unit.level]['increase']))
                    unit_data['shield'] = int(round(unit_data['shield'] + unit_data['shield'] * settings.UNIT_UPDATE[unit.level]['increase']))
                    unit_data['attack'] = int(round(unit_data['attack'] + unit_data['attack'] * settings.UNIT_UPDATE[unit.level]['increase']))
                    unit_data['critical_chance'] = round(unit_data['critical_chance'] + unit_data['critical_chance'] * settings.UNIT_UPDATE[unit.level]['increase'])

                    unit_data['critical_ratio'] = round(unit_data['critical_ratio'] + unit_data['critical_ratio'] * settings.UNIT_UPDATE[unit.level]['increase'])

                    unit_data['miss_chance'] = round(unit_data['miss_chance'] + unit_data['miss_chance'] * settings.UNIT_UPDATE[unit.level]['increase'])

                    unit_data['dodge_chance'] = round(unit_data['dodge_chance'] + unit_data['dodge_chance'] * settings.UNIT_UPDATE[unit.level]['increase'])

                unit_data['quantity'] = unit.quantity

                unit_data['next_upgrade_stats'] = {
                    'card_cost': settings.UNIT_UPDATE[unit.level + 1]['coins'],
                    'card_count': settings.UNIT_UPDATE[unit.level + 1]['unit_cards'],
                    'attack': unit_data['attack'] + unit_data['attack'] * settings.UNIT_UPDATE[unit.level + 1]['increase'],
                    'health': unit_data['health'] + unit_data['health'] * settings.UNIT_UPDATE[unit.level + 1]['increase'],
                    'shield': unit_data['shield'] + unit_data['shield'] * settings.UNIT_UPDATE[unit.level + 1]['increase'],
                    'critical_chance': unit_data['critical_chance'] + unit_data['critical_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'],
                    'critical_ratio': unit_data['critical_ratio'] + unit_data['critical_ratio'] * settings.UNIT_UPDATE[unit.level + 1]['increase'],
                    'miss_chance': unit_data['miss_chance'] + unit_data['miss_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'],
                    'dodge_chance': unit_data['dodge_chance'] + unit_data['dodge_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase']
                }

                unit_data['level'] = unit.level
                unit_data['cool_down'] = unit.is_cool_down
                unit_data['cool_down_remaining_seconds'] = 0
                # TODO set cooldown remaining
                list_unit.append(unit_data)

            data['units'] = list_unit

            list_item = []
            for item in UserItem.objects.filter(item__hero=hero_user.hero, user=requests):
                item_serializer = ItemSerializer(item.item)
                item_data = item_serializer.data

                item_data['next_upgrade_stats'] = {
                    'card_cost': settings.ITEM_UPDATE[item.level + 1]['coins'],
                    'card_count': settings.ITEM_UPDATE[item.level + 1]['item_cards'],
                    'damage': int(round(item_data['damage'] + item_data['damage'] * settings.ITEM_UPDATE[item.level + 1]['increase'])),
                    'health': int(round(item_data['health'] + item_data['health'] * settings.ITEM_UPDATE[item.level + 1]['increase'])),
                    'shield': int(round(item_data['shield'] + item_data['shield'] * settings.ITEM_UPDATE[item.level + 1]['increase'])),
                    'critical_chance': round(item_data['critical_chance'] + item_data['critical_chance'] *settings.ITEM_UPDATE[item.level + 1]['increase']),
                    'critical_ratio': round(item_data['critical_ratio'] + item_data['critical_ratio'] * settings.ITEM_UPDATE[item.level + 1]['increase'])
                }

                item_data['quantity'] = item.quantity
                item_data['next_upgrade_card_cost'] = settings.ITEM_UPDATE[item.level + 1]['coins']
                item_data['next_upgrade_card_count'] = settings.ITEM_UPDATE[item.level + 1]['item_cards']
                item_data['level'] = item.level

                if data['selected_hero']:
                    item_data['selected_item'] = True if item.item.id in \
                                                         UserHero.get_selected_item(requests, hero_user.hero) else False
                else:
                    item_data['selected_item'] = False

                list_item.append(item_data)

            data['items'] = list_item
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
                    'attack': int(round(hero_user.hero.chakra_attack + hero_user.hero.chakra_attack * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),
                    'health': int(round(hero_user.hero.chakra_health + hero_user.hero.chakra_health * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),
                    'shield': int(round(hero_user.hero.chakra_shield + hero_user.hero.chakra_shield * settings.HERO_UPDATE[hero_user.level + 1]['increase'])),
                    'critical_chance': round(hero_user.hero.chakra_critical_chance + hero_user.hero.chakra_critical_chance * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),
                    'critical_ratio': round(hero_user.hero.chakra_critical_ratio + hero_user.hero.chakra_critical_ratio * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),
                    'miss_chance': round(hero_user.hero.chakra_miss_chance + hero_user.hero.chakra_miss_chance * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2),
                    'dodge_chance': round(hero_user.hero.chakra_dodge_chance + hero_user.hero.chakra_dodge_chance * settings.HERO_UPDATE[hero_user.level + 1]['increase'], 2)


            }
            }

            list_serialize.append(data)

        return list_serialize

    def get_general_units(self, requests):
        hero_units = list(HeroUnits.objects.all().values_list('unit_id', flat=True))

        list_unit = []
        for unit in UserCard.objects.filter(user=requests).exclude(character_id__in=hero_units):
            serializer = UnitSerializer(unit.character)
            data = serializer.data

            if unit.level in settings.UNIT_UPDATE.keys():
                data['health'] = int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[unit.level]['increase']))
                data['shield'] = int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[unit.level]['increase']))
                data['attack'] = int(round(data['attack'] + data['attack'] * settings.UNIT_UPDATE[unit.level]['increase']))
                data['critical_chance'] = round(data['critical_chance'] + data['critical_chance'] * settings.UNIT_UPDATE[unit.level]['increase'], 2)
                data['critical_ratio'] = round(data['critical_ratio'] + data['critical_ratio'] * settings.UNIT_UPDATE[unit.level]['increase'], 2)
                data['miss_chance'] = round(data['miss_chance'] + data['miss_chance'] * settings.UNIT_UPDATE[unit.level]['increase'], 2)
                data['dodge_chance'] = round(data['dodge_chance'] + data['dodge_chance'] * settings.UNIT_UPDATE[unit.level]['increase'], 2)

            data['quantity'] = unit.quantity

            data['next_upgrade_stats'] = {
                'card_cost': settings.UNIT_UPDATE[unit.level + 1]['coins'],
                'card_count': settings.UNIT_UPDATE[unit.level + 1]['unit_cards'],
                'attack': int(round(data['attack'] + data['attack'] * settings.UNIT_UPDATE[unit.level + 1]['increase'])),
                'health': int(round(data['health'] + data['health'] * settings.UNIT_UPDATE[unit.level + 1]['increase'])),
                'shield': int(round(data['shield'] + data['shield'] * settings.UNIT_UPDATE[unit.level + 1]['increase'])),
                'critical_chance': round(data['critical_chance'] + data['critical_chance'] *settings.UNIT_UPDATE[unit.level + 1]['increase'], 2),
                'critical_ratio': round(data['critical_ratio'] + data['critical_ratio'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2),
                'miss_chance': round(data['miss_chance'] + data['miss_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2),
                'dodge_chance': round(data['dodge_chance'] + data['dodge_chance'] * settings.UNIT_UPDATE[unit.level + 1]['increase'], 2)
            }
            data['level'] = unit.level
            list_unit.append(data)

        return list_unit

    # def create(self, validated_data):
    #     # if 'email' not in validated_data:
    #     #     raise serializers.ValidationError({"id": 400, "message": "email required"})
    #
    #     user = get_user_model().objects.create_user(**validated_data)
    #     return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super(UserSerializer, self).update(instance, validated_data)

    def get_newsletter(self, requests):
        lst_news = []

        for inbox in Inbox.user_inbox.filter(user=requests):
            serializer = NewsLetterSerializer(inbox.news)
            data = serializer.data
            data['status'] = inbox.message_type
            lst_news.append(data)

        return lst_news


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitBox
        fields = (
            'id',
            'name',
            'box',
            'quantity'
        )


class ChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chest
        fields = (
            'chest_type',
            'min_coin',
            'max_coin',
            'min_gem',
            'max_gem',
            'new_card_chance',
            'hero_card',
            'unit_card'
        )


class LeagueInfoSerializer(serializers.ModelSerializer):
    chests = ChestSerializer(many=True, read_only=True)

    class Meta:
        model = LeagueInfo
        fields = (
            'id',
            'name',
            'min_score',
            'chests',
            'description'
        )


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = (
            'id',
            'name',
            'coins',
            'gems',
            'chests',
            'special_offer'
        )
