import uuid
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, BenefitSerializer, LeagueInfoSerializer, \
    ShopSerializer, UserChestSerializer, UserCardSerializer, UserHeroSerializer, ItemSerializer, UserCurrencySerializer, \
    UnitSerializer, HeroSerializer, AppConfigSerializer
from objects.models import BenefitBox, UserBuy, UserCurrency, Hero, UserHero, \
    LeagueInfo, UserChest, UserCard, Unit, UserItem, Item, AppConfig
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from shopping.models import Shop
from django.conf import settings
from common.utils import ChestGenerate, hero_normalize_data, unit_normalize_data, item_normalize_data


class DefaultsMixin(object):
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class AuthMixin(object):
    authentication_classes = (
        TokenAuthentication,
        JSONWebTokenAuthentication
    )

    permission_classes = (
        IsAuthenticated,
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()

    def create(self, request, *args, **kwargs):
        player_id = str(uuid.uuid1().int >> 32)
        User.objects.create_user(username=player_id, password=player_id)
        return Response({'id': 201, 'player_id': player_id}, status=status.HTTP_201_CREATED)

    @list_route(methods=['POST'])
    def select_hero(self, request):
        if request.data.get('hero') is None:
            return Response(
                {'id': 400, 'message': 'no selected hero'}, status=status.HTTP_400_BAD_REQUEST)

        hero = get_object_or_404(Hero, id=request.data.get('hero'))
        user_hero, created = UserHero.objects.get_or_create(user=request.user, hero=hero)
        UserHero.objects.filter(user=request.user).exclude(id=user_hero.id).update(enable_hero=False)
        user_hero.enable_hero = True
        user_hero.save()

        return Response(
            {'id': 200, 'message': 'ok'}, status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    def player_info(self, request):
        user = get_object_or_404(User, id=request.user.id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def open_chest(self, request):
        chest = get_object_or_404(UserChest, pk=request.data.get('id'), user=request.user, status='close')

        if UserChest.deck.filter(user=request.user, status='opening').count() >= 1:
            return Response({'id': 404, 'message': 'deck is full'}, status=status.HTTP_400_BAD_REQUEST)

        chest.chest_opening_date = datetime.now() + timedelta(
            hours=settings.CHEST_SEQUENCE_TIME[chest.chest.chest_type])

        chest.chest_status = 'opening'
        chest.save()

        return Response({'id': 201, 'message': 'chest change status opening'}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def use_skip_gem(self, request):
        chest = get_object_or_404(UserChest, pk=request.data.get('id'), user=request.user, status='opening')

        if chest.skip_gem > UserCurrency.hard_currency(request.user):
            return Response({'id': 400, 'message': 'gem not enough'}, status=status.HTTP_400_BAD_REQUEST)

        UserCurrency.subtract(request.user, chest.skip_gem, 'GEM')

        chest.chest_status = 'ready'
        chest.save()

        return Response({'id': 201, 'message': 'chest change status ready'}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def chest_ready(self, request):
        chest = get_object_or_404(UserChest, pk=request.data.get('id'), user=request.user, status='ready')
        serializer = UserChestSerializer(chest)
        UserCurrency.update_currency(request.user, chest.cards['gems'], chest.cards['coins'])
        for unit in chest.reward_data['units']:
            character = Unit.objects.get(moniker=unit['unit'])
            UserCard.upgrade_character(request.user, character, unit['count'])

        # TODO add hero card
        # TODO add item card

        chest.status = 'used'
        chest.save()

        return Response({'id': 201, 'chest': serializer.data}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def set_player_name(self, request):
        try:
            name = request.data.get('name')
            profile = UserCurrency.objects.get(name=name)
            name = '{}{}'.format(name, str(uuid.uuid1().int >> 5))

        except:
            name = request.data.get('name')

        finally:
            profile = UserCurrency.objects.get(user=request.user)
            profile.name = name
            profile.save()

        return Response({'id': 201, 'user_name': name}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def change_player_name(self, request):
        if request.user.user_currency.can_change_name:
            try:
                name = request.data.get('name')
                profile = UserCurrency.objects.get(name=name)
                return Response({'id': 400, 'message': 'name already exists', 'name': profile.name}, status=status.HTTP_400_BAD_REQUEST)

            except:
                profile = UserCurrency.objects.get(user=request.user)
                profile.name = name
                profile.can_change_name = False
                profile.save()

            return Response({'id': 200, 'message': 'name changed', 'name': profile.name}, status=status.HTTP_200_OK)

        return Response({'id': 400, 'message': 'cant change name'}, status=status.HTTP_400_BAD_REQUEST)


class LeagueViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LeagueInfo.objects.all()
    serializer_class = LeagueInfoSerializer


class ShopViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @list_route(methods=['POST'])
    def store(self, request):
        shop_item = Shop.objects.filter(store_id=request.data.get('store_id'), enable=True).first()
        serializer = self.serializer_class(shop_item)
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def buy_gem(self, request):
        shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

        store = (item for item in shop.gems if item['id'] == request.data.get('id')).next()
        # TODO check store api
        request.user.user_currency.gem += store['amount']
        request.user.user_currency.save()

        return Response({'buy_gem': store['amount'], 'user_gem': request.user.user_currency.gem}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def buy_coin(self, request):
        shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

        store = (item for item in shop.coins if item['id'] == request.data.get('id')).next()
        if request.user.user_currency.gem >= store['price']:
            request.user.user_currency.gem -= store['price']
            request.user.user_currency.coin += store['amount']
            request.user.user_currency.save()

            return Response({
                'buy_coin': store['amount'],
                'user_coin': request.user.user_currency.coin,
                'used_gem': store['price'],
                'user_gem': request.user.user_currency.gem
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'id': 400, 'message': 'gem not enough'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def buy_chest(self, request):
        chest_type = {
            'wooden': 'W',
            'silver': 'S',
            'gold': 'G',
            'crystal': 'C'
        }
        shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

        store = (item for item in shop.chests if item['id'] == request.data.get('id')).next()
        if request.user.user_currency.gem >= store['price']:
            request.user.user_currency.gem -= store['price']
            request.user.user_currency.save()

            chest = ChestGenerate(request.user, chest_type[store['type']])
            chest_value = chest.generate_chest()
            UserCurrency.update_currency(request.user, chest_value['gems'], chest_value['coins'])

            for unit in chest_value['units']:
                character = Unit.objects.get(moniker=unit['unit'])
                UserCard.upgrade_character(request.user, character, unit['count'])

            return Response(chest_value)

        return Response({'id': 400, 'message': 'gems are not enough'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def buy_special_offer(self, request):
        chest_type = {
            'wooden': 'W',
            'silver': 'S',
            'gold': 'G',
            'crystal': 'C'
        }
        shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

        store = (item for item in shop.special_offer if item['id'] == request.data.get('id')).next()
        # TODO check store api
        chst_lst = []
        chst_item = []

        for offer_chest in store['chests']:
            chest = ChestGenerate(request.user, chest_type[offer_chest['type']])
            chest_value = chest.generate_chest()
            UserCurrency.update_currency(request.user, chest_value['gems'], chest_value['coins'])

            for unit in chest_value['units']:
                character = Unit.objects.get(moniker=unit['unit'])
                UserCard.upgrade_character(request.user, character, unit['count'])

            chest_item = {'chest_reward': chest_value}
            chst_lst.append(chest_item)

        UserCurrency.update_currency(request.user, store['gem'], store['coin'])

        result = {
            'gems': store['gem'],
            'coins': store['coin'],
            'chests': chst_lst
        }

        return Response(result)


class UserChestViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = UserChest.objects.all()
    serializer_class = UserChestSerializer

    @list_route(methods=['POST'])
    def generate_win_chest(self, request):
        if not UserChest.deck_is_open(request.user, 'non_free'):
            return Response({'message': 'deck is full'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        chest_gen = ChestGenerate(request.user)
        chest_gen.generate_chest()
        return Response({'message': 'chest generated'}, status=status.HTTP_200_OK)


class UserCardViewSet(DefaultsMixin, AuthMixin, viewsets.GenericViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer

    @list_route(methods=['POST'])
    def level_up(self, request):
        unit_id = request.data.get('unit_id')
        user_card = get_object_or_404(UserCard, user=request.user, character_id=unit_id)
        user_currency = get_object_or_404(UserCurrency, user=request.user)

        next_level = settings.UNIT_UPDATE[user_card.level + 1]

        if user_card.quantity < next_level['unit_cards']:
            return Response({'message': 'card not enough'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if user_currency.coin < next_level['coins']:
            return Response({'message': 'coins not enough'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user_currency.coin -= next_level['coins']
        user_currency.save()

        user_card.quantity -= next_level['unit_cards']
        user_card.save()

        user_card.level += 1
        user_card.save()

        serializer = UnitSerializer(user_card.character)
        data = unit_normalize_data(user_card, serializer.data)

        return Response(data, status=status.HTTP_200_OK)


class UserHeroViewSet(DefaultsMixin, AuthMixin, viewsets.GenericViewSet):
    queryset = UserHero.objects.all()
    serializer_class = UserHeroSerializer

    @list_route(methods=['POST'])
    def level_up(self, request):
        hero_id = request.data.get('hero_id')
        user_hero = get_object_or_404(UserHero, user=request.user, hero_id=hero_id)
        user_currency = get_object_or_404(UserCurrency, user=request.user)

        next_level = settings.HERO_UPDATE[user_hero.level + 1]

        if user_hero.quantity < next_level['hero_cards']:
            return Response({'message': 'card not enough'}, status=status.HTTP_200_OK)

        if user_currency.coin < next_level['coins']:
            return Response({'message': 'coins not enough'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user_currency.coin -= next_level['coins']
        user_currency.save()

        user_hero.quantity -= next_level['hero_cards']
        user_hero.save()

        user_hero.level += 1
        user_hero.save()

        serializer = HeroSerializer(user_hero.hero)
        data = hero_normalize_data(user_hero, serializer.data)

        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=['POST'])
    def selected_items(self, request):
        list_items = request.data.get('list_items')
        user_hero = get_object_or_404(UserHero, user=request.user, enable_hero=True)

        selected_items = []

        for lst_itm in list_items:
            item = Item.objects.get(pk=lst_itm)

            if item.hero == user_hero.hero:
                serializer = ItemSerializer(item)
                selected_items.append(serializer.data)

            else:
                return Response({'id': 404, 'message': 'hero selected item not found'},
                                status=status.HTTP_404_NOT_FOUND)

        user_hero.selected_item = selected_items
        user_hero.save()

        return Response({'id': 200, 'message': 'hero selected item updated'}, status=status.HTTP_200_OK)


class UserItemViewset(DefaultsMixin, AuthMixin, viewsets.GenericViewSet):
    queryset = UserItem.objects.all()
    serializer_class = ItemSerializer

    @list_route(methods=['POST'])
    def level_up(self, request):
        item_id = request.data.get('item_id')
        user_item = get_object_or_404(UserItem, user=request.user, item_id=item_id)
        user_currency = get_object_or_404(UserCurrency, user=request.user)

        next_level = settings.ITEM_UPDATE[user_item.level + 1]

        if user_item.quantity < next_level['item_cards']:
            return Response({'message': 'card not enough'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        if user_currency.coin < next_level['coins']:
            return Response({'message': 'coins not enough'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        user_currency.coin -= next_level['coins']
        user_currency.save()

        user_item.quantity -= next_level['item_cards  ']
        user_item.save()

        user_item.level += 1
        user_item.save()

        serializer = ItemSerializer(user_item.item)
        data = item_normalize_data((user_item, serializer.data))

        return Response(data, status=status.HTTP_200_OK)


class AppConfigViewSet(viewsets.ModelViewSet):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer