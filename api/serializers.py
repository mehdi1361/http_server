from django.contrib.auth import get_user_model
from rest_framework import serializers
from objects.models import BenefitBox, UserCurrency, Hero, Unit, UserHero, HeroUnits, UserCard, LeagueInfo, Chest
from shopping.models import Shop


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCard
        fields = ('name', 'quantity')

    def get_name(self, requests):
        return self.character.id


class UserCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCurrency
        fields = ('gem', 'coin')


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ('moniker',
                  'dexterity',
                  'attack_type',
                  'attack',
                  'critical_chance',
                  'critical_ratio',
                  'level',
                  'miss_chance',
                  'enable_in_start'
                  )


class HeroSerializer(serializers.ModelSerializer):
    # units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Hero
        fields = ('moniker', 'dexterity', 'attack_type', 'health', 'level', 'chakra_health', 'shield', 'chakra_shield',
                  'attack', 'chakra_attack', 'critical_chance', 'chakra_critical_chance', 'chakra_critical_ratio',
                  'critical_ratio', 'miss_chance', 'chakra_miss_chance', 'chakra_dodge_chance', 'enable_in_start')


class UserSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    heroes = serializers.SerializerMethodField()
    general_units = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'email',
            'currency',
            'currency',
            'heroes',
            'general_units'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_currency(self, request):
        try:
            currency = UserCurrency.objects.get(user=self.context['request'].user)
            serializer = UserCurrencySerializer(currency)
            return serializer.data

        except UserCurrency.DoesNotExist as e:
            return None

    def get_heroes(self, request):
        try:
            hero_user = UserHero.objects.get(user=self.context['request'].user, enable_hero=True)

        except UserHero.DoesNotExist as e:
            hero_user = None

        finally:
            list_serialize = []
            for hero in Hero.objects.all():
                serializer = HeroSerializer(hero)
                data = serializer.data

                if hero.id == hero_user.id:
                    data['selected_hero'] = True

                else:
                    data['selected_hero'] = False

                data['quantity'] = hero_user.quantity
                data['next_upgrade_coin_cost'] = hero_user.next_upgrade_coin_cost
                data['next_upgrade_card_count'] = hero_user.next_upgrade_card_count

                list_unit = []
                for unit in UserCard.objects.filter(character__heroes=hero):
                    unit_serializer = UnitSerializer(unit.character)
                    unit_data = unit_serializer.data
                    unit_data['quantity'] = unit.quantity
                    unit_data['next_upgrade_coin_cost'] = unit.next_upgrade_coin_cost
                    unit_data['next_upgrade_card_count'] = unit.next_upgrade_card_count
                    unit_data['level'] = unit.level
                    list_unit.append(unit_data)

                data['units'] = list_unit
                list_serialize.append(data)

            return list_serialize

    def get_general_units(self, requests):
        hero_units = list(HeroUnits.objects.all().values_list('unit_id', flat=False))
        # units = Unit.objects.all().exclude(id__in=hero_units)

        list_unit = []
        for unit in UserCard.objects.exclude(character_id__in=hero_units):
            serializer = UnitSerializer(unit.character)
            data = serializer.data
            data['quantity'] = unit.quantity
            data['next_upgrade_coin_cost'] = unit.next_upgrade_coin_cost
            data['next_upgrade_card_count'] = unit.next_upgrade_card_count
            data['level'] = unit.level
            list_unit.append(data)

        return list_unit

    def create(self, validated_data):
        if 'email' not in validated_data:
            raise serializers.ValidationError({"id": 400, "message": "email required"})

        user = get_user_model().objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super(UserSerializer, self).update(instance, validated_data)


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BenefitBox
        fields = (
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
