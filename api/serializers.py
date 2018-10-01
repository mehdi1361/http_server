from django.contrib.auth import get_user_model
from rest_framework import serializers
from objects.models import BenefitBox, UserCurrency, Hero, Unit, UserHero, HeroUnits, UserCard, \
    LeagueInfo, Chest, UserChest, Item, UserItem, AppConfig, LeagueUser, LeaguePrize, League, Claim, LeagueTime
from shopping.models import Shop
from message.models import NewsLetter, Inbox
from common.utils import hero_normalize_data, unit_normalize_data, item_normalize_data


def unlock_league(unit):
    league = League.objects.filter(ctm_chests__units__unit=unit, ctm_chests__units__enable=True)\
        .order_by('step_number').first()

    step_number = 0
    if league.league_name in ['Cooper01', 'Silver01', 'Gold01']:
        step_number = 0

    if league.league_name in ['Cooper02', 'Silver02', 'Gold02']:
        step_number = 1

    # if league.league_name in ['Cooper03', 'Silver01', 'Gold01']:
    #     step_number = 2

    result = {
        'league': league.league_type,
        'step_number': step_number
    }
    return result


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


class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'news',
            'message_type',
            'user'
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
            'tutorial_done', 
            'next_session_remaining_seconds',
            'google_account',
            'google_id'

        )


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = (
            'capacity',
            'league_step',
            'league_type',
            'min_trophy',
            'playoff_range',
            'playoff_count'
        )


class LeaguePrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaguePrize
        fields = (
            'gem',
            'coin',
            'level'
        )


class LeagueUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeagueUser
        fields = (
            'score',
            'rank',
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
            'shield',
            'unlock'
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
            # 'max_health',
            # 'max_shield'
        )


class UserCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
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
    google_id = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'google_id',
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

            result = serializer.data

            if LeagueUser.has_league(requests.user_currency):
                result['in_league'] = True
                result['trophy'] = LeagueUser.player_score(requests.user_currency)

            else:
                result['in_league'] = False
                result['trophy'] = 0

            result['current_league'] = None
            try:
                league = LeagueUser.objects.get(player=requests.user_currency, close_league=False)
                current_league = LeagueSerializer(league.league.base_league)
                result['current_league'] = current_league.data

            except LeagueUser.DoesNotExist:
                result['current_league'] = None

            result['league_time'] = LeagueTime.remain_time()
            return result

        except UserCurrency.DoesNotExist as e:
            return None

    def get_heroes(self, requests):
        list_serialize = []
        for hero_user in UserHero.objects.filter(user=requests):
            serializer = HeroSerializer(hero_user.hero)
            data = hero_normalize_data(hero_user, serializer.data)

            list_unit = []
            for unit in UserCard.objects.filter(
                    character__heroes=hero_user.hero,
                    user=requests,
                    character__coming_soon=True
            ):
                unit_serializer = UnitSerializer(unit.character)
                unit_data = unit_normalize_data(unit, unit_serializer.data)
                list_unit.append(unit_data)

            data['units'] = list_unit

            list_item = []
            for item in UserItem.objects.filter(item__hero=hero_user.hero, user=requests):
                item_serializer = ItemSerializer(item.item)
                item_data = item_normalize_data(item, item_serializer.data)

                if data['selected_hero']:
                    item_data['selected_item'] = True if item.item.id in \
                                                    UserHero.get_selected_item(requests, hero_user.hero) else False
                else:
                    data['selected_item'] = False
                list_item.append(item_data)

            data['items'] = list_item

            list_serialize.append(data)

        return list_serialize

    def get_general_units(self, requests):
        hero_units = list(HeroUnits.objects.all().values_list('unit_id', flat=True))

        list_unit = []
        for unit in UserCard.objects.filter(user=requests, character__unlock=True)\
                .exclude(character_id__in=hero_units):
            serializer = UnitSerializer(unit.character)
            data = unit_normalize_data(unit, serializer.data)
            league = unlock_league(unit.character)
            data['unlock_league'] = league['league']
            data['unlock_league_step_number'] = league['step_number']
            data['used_status'] = 'unlock'
            list_unit.append(data)

        for unit in UserCard.objects.filter(user=requests, character__coming_soon=True)\
                .exclude(character_id__in=hero_units):
            serializer = UnitSerializer(unit.character)
            data = unit_normalize_data(unit, serializer.data)
            league = unlock_league(unit.character)
            data['unlock_league'] = league['league']
            data['unlock_league_step_number'] = league['step_number']
            data['used_status'] = 'coming_soon'
            list_unit.append(data)

        return list_unit

    def get_google_id(self, requests):
        return requests.user_currency.google_id


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
            'chests'
        )


class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        fields = ('app_data', )


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = (
            'coin',
            'gem',
        )