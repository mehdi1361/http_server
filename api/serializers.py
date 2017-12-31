from django.contrib.auth import get_user_model
from rest_framework import serializers
from objects.models import BenefitBox, UserChest, Hero, Unit, UserHero, HeroUnits, UserCard
# from django.contrib.auth.models import User


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCard
        fields = ('name', 'quantity')

    def get_name(self, requests):
        return self.character.id


class UserChestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChest
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
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Hero
        fields = ('moniker', 'dexterity', 'attack_type', 'health', 'level', 'chakra_health', 'shield', 'chakra_shield',
                  'attack', 'chakra_attack', 'critical_chance', 'chakra_critical_chance', 'chakra_critical_ratio',
                  'critical_ratio', 'miss_chance', 'chakra_miss_chance', 'chakra_dodge_chance', 'enable_in_start',
                  'units')


class UserSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()
    heroes = serializers.SerializerMethodField()
    general_units = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

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
            'general_units',
            'cards'
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_currency(self, request):
        try:
            currency = UserChest.objects.get(user=self.context['request'].user)
            serializer = UserChestSerializer(currency)
            return serializer.data

        except UserChest.DoesNotExist as e:
            return None

    def get_heroes(self, request):
        try:
            hero_user = UserHero.objects.get(user=self.context['request'].user, enable_hero=False)

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

                list_serialize.append(data)

            return list_serialize

    def get_general_units(self, requests):
        hero_units = list(HeroUnits.objects.all().values_list('unit_id', flat=True))
        units = Unit.objects.all().exclude(id__in=hero_units)
        serializer = UnitSerializer(units, many=True)
        data = serializer.data
        return data

    def get_cards(self, requests):
        list_cards = []
        for cards in UserCard.objects.filter(user=self.context['request'].user):
            list_cards.append(
                {
                    "id": cards.character.id,
                    "name": cards.character.moniker,
                    "quantity": cards.quantity,
                    "next_upgrade_coin_cost": cards.next_upgrade_coin_cost,
                    "next_upgrade_card_count": cards.next_upgrade_card_count,
                    "level": cards.level
                })

        return list_cards

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
