import uuid
import time
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import AllowAny

from message.models import Inbox
from .serializers import UserSerializer, BenefitSerializer, LeagueInfoSerializer, \
    ShopSerializer, UserChestSerializer, UserCardSerializer, UserHeroSerializer, ItemSerializer, UserCurrencySerializer, \
    UnitSerializer, HeroSerializer, AppConfigSerializer, InboxSerializer, LeaguePrizeSerializer, LeagueUserSerializer, \
    LeagueSerializer, ClaimSerializer
from objects.models import Device, UserCurrency, Hero, UserHero, \
    LeagueInfo, UserChest, UserCard, Unit, UserItem, Item, AppConfig, LeagueUser, League, Claim, \
    PlayOff, LeagueTime, LeaguePrize
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from shopping.models import Shop
from django.conf import settings
from common.utils import hero_normalize_data, \
    unit_normalize_data, item_normalize_data, CtmChestGenerate
from common.video_ads import VideoAdsFactory
from shopping.models import PurchaseLog, CurrencyLog
from common.payment_verification import CafeBazar, FactoryStore
from reports.models import Battle
from django.db.models import Q
from operator import itemgetter


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
        device_id = request.data['deviceUniqueID']
        device_name = request.data['deviceName']

        player_id = str(uuid.uuid1().int >> 32)
        user = User.objects.create_user(username=player_id, password=player_id)
        chest = CtmChestGenerate(user)
        profile = UserCurrency.objects.get(user_id=user.id)
        Device.objects.create(device_model=device_name, device_id=device_id, user=profile)
        chest.generate_tutorial_chest()
        return_id = 201

        return Response(
            {'id': return_id, 'player_id': player_id},
            status=status.HTTP_201_CREATED if return_id == 201 else status.HTTP_200_OK
        )

    @list_route(methods=['POST'])
    def select_hero(self, request):
        if request.data.get('hero') is None:
            return Response(
                {'id': 400, 'message': 'no selected hero'}, status=status.HTTP_400_BAD_REQUEST)

        hero = get_object_or_404(Hero, id=request.data.get('hero'))
        user_hero, created = UserHero.objects.get_or_create(user=request.user, hero=hero)
        UserHero.objects.filter(user=request.user).exclude(id=user_hero.id).update(enable_hero=False)
        user_hero.enable_hero = True
        user_hero.level = 1
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

        if chest.chest_monetaryType == 'free':
            opening_date = datetime.now() + timedelta(seconds=5)

        else:
            opening_date = datetime.now() + timedelta(hours=settings.CHEST_SEQUENCE_TIME[chest.chest.chest_type])

        chest.chest_opening_date = opening_date

        chest.chest_status = 'opening'
        chest.save()

        return Response({'id': 201, 'message': 'chest change status opening'}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def use_skip_gem(self, request):
        chest = get_object_or_404(UserChest, pk=request.data.get('id'), user=request.user, status='opening')

        if chest.skip_gem > UserCurrency.hard_currency(request.user):
            return Response({'id': 400, 'message': 'gem not enough'}, status=status.HTTP_400_BAD_REQUEST)

        UserCurrency.subtract(request.user, chest.skip_gem, 'GEM')

        profile = UserCurrency.objects.get(user=request.user)
        CurrencyLog.objects.create(
            user=profile,
            type='GEM',
            quantity_used=chest.skip_gem,
            type_buy='SKIP_GEM',
            quantity_buy=1
        )

        chest.chest_status = 'ready'
        chest.save()

        return Response({'id': 201, 'message': 'chest change status ready'}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def chest_ready(self, request):
        chest = get_object_or_404(UserChest, pk=request.data.get('id'), user=request.user)
        if chest.status != 'ready':
            print(chest.remain_time)
            if chest.remain_time <= 0:
                chest.status = 'ready'
                chest.save()
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserChestSerializer(chest)
        UserCurrency.update_currency(request.user, chest.reward_data['gems'], chest.reward_data['coins'])
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
        name = request.data.get('name')
        try:
            user_profile = UserCurrency.objects.get(name=name)
            name = '{}{}'.format(name, str(uuid.uuid1().int >> 5))[:18]

        except Exception:

            name = request.data.get('name')

        finally:
            profile = UserCurrency.objects.get(user=request.user)
            profile.name = name
            profile.save()

        return Response({'id': 201, 'user_name': name}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def set_tutorial_done(self, request):
        profile = UserCurrency.objects.get(user=request.user)
        profile.tutorial_done = True
        profile.save()

        return Response({'id': 201, 'tutorial_done': True}, status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def change_player_name(self, request):
        if request.user.user_currency.can_change_name:
            try:
                name = request.data.get('name')
                profile = UserCurrency.objects.get(name=name)
                return Response({'id': 400, 'message': 'name already exists', 'name': profile.name},
                                status=status.HTTP_400_BAD_REQUEST)

            except:
                profile = UserCurrency.objects.get(user=request.user)
                profile.name = name
                profile.can_change_name = False
                profile.save()

            return Response({'id': 200, 'message': 'name changed', 'name': profile.name}, status=status.HTTP_200_OK)

        return Response({'id': 400, 'message': 'cant change name'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def leader_board(self, request):
        final_result = dict()
        previous_rank = None
        current_rank = None
        try:
            league = LeagueUser.objects.get(player=request.user.user_currency, close_league=False)
            score_board = []
            idx = 1

            for user in LeagueUser.objects.in_league().filter(league=league.league).order_by('-score'):
                serializer = LeagueUserSerializer(user)

                result = serializer.data
                if user.player == request.user.user_currency:
                    previous_rank = result['rank'] if result['rank'] else idx
                    current_rank = idx
                    user.rank = idx
                    user.save()

                result['rank'] = idx
                result['player'] = str(user.player).decode('utf-8')
                idx += 1
                score_board.append(result)

            if len(score_board) < league.league.base_league.capacity:
                fake_count = league.league.base_league.capacity - len(score_board)

                for i in range(0, fake_count):
                    score_board.append(
                        {
                            'score': league.league.params['fake_user'][i]['score'],
                            'rank': 0,
                            'player': league.league.params['fake_user'][i]['name']
                        }
                    )

                score_board = sorted(score_board, key=itemgetter('score'), reverse=True)

                for idx, item in enumerate(score_board):
                    item['rank'] = idx + 1
                    if item['player'] == request.user.user_currency.name:
                        previous_rank = league.rank if league.rank else idx
                        current_rank = idx
                        league.rank = idx + 1
                        league.save()

            prize_serializer = LeaguePrizeSerializer(league.league.base_league.prizes, many=True)

            current_league = LeagueSerializer(league.league.base_league)

            max_step = League.objects.all().values('step_number').order_by('-step_number')[0]

            if max_step['step_number'] > league.league.base_league.step_number + 1:
                next_league = League.objects.get(step_number=league.league.base_league.step_number + 1)
                next_league_serializer = LeagueSerializer(next_league)

            else:
                next_league_serializer = LeagueSerializer(current_league)

            final_result['score_board'] = score_board
            final_result['promoting_prize'] = prize_serializer.data
            final_result['previous_rank'] = previous_rank
            final_result['current_rank'] = current_rank
            final_result['current_league'] = current_league.data
            final_result['next_league'] = next_league_serializer.data
            final_result['num_of_promoting_user'] = league.league.base_league.promoting_count
            final_result['num_of_demoting_user'] = league.league.base_league.demoting_count

            final_result['league_change_status'] = league.league_change_status

            if league.league_change_status == 'promoted':
                previous_league = LeagueUser.objects.get(
                    player=request.user.user_currency,
                    close_league=True,
                    league__base_league__step_number=league.league.base_league.step_number - 1
                )
                claim = Claim.objects.get(is_used=False, league_player=previous_league)
                claim_serializer = ClaimSerializer(claim)
                final_result['league_change_prize'] = claim_serializer.data

            else:
                final_result['league_change_prize'] = None

            if league.score >= league.league.base_league.play_off_unlock_score:
                    if league.play_off_status != 'start':
                        league.play_off_status = 'not_started'

            else:
                league.play_off_status = 'disable'

            league.save()

            if league.play_off_count <= 1:
                play_off_count = league.league.base_league.play_off_start_gem

            elif league.play_off_count == 2:
                play_off_count = league.league.base_league.play_off_start_gem_1

            else:
                play_off_count = league.league.base_league.play_off_start_gem_2

            final_result['play_off_info'] = {
                "status": league.play_off_status,
                "start_gem_price": play_off_count,
                "unlock_need_score": league.league.base_league.play_off_unlock_score,
                "result": [] if PlayOff.log(request.user.user_currency) == -1
                else PlayOff.log(request.user.user_currency),
                "num_wins": league.league.base_league.win_promoting_count
            }
            final_result['remain_time'] = LeagueTime.remain_time()


            prizes = []
            for league in League.objects.all().order_by('step_number'):
                prizes.append({
                    "gem": league.params['play_off_reward']['gem'] if league.params is not None else None,
                    "coin": league.params['play_off_reward']['coin']} if league.params is not None else None
                )

            final_result['leagues_rewards'] = prizes

            return Response(final_result)

        except Exception as e:
            return Response({"id": 400, "message": e}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def has_league(self, request):
        if LeagueUser.has_league(request.user.user_currency):
            return Response({'id': 200, 'message': 'player joined to league'}, status=status.HTTP_200_OK)

        return Response({'id': 400, 'message': 'player not yet joined to league'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def active_playoff(self, request):
        try:
            league = LeagueUser.objects.get(
                player=request.user.user_currency,
                close_league=False, play_off_status="not_started"
            )

            if league.score >= league.league.base_league.play_off_unlock_score:

                if league.league.base_league.playoff_count <= 1:
                    if request.user.user_currency.gem >= league.league.base_league.play_off_start_gem:
                        request.user.user_currency.gem -= league.league.base_league.play_off_start_gem
                        request.user.user_currency.save()

                    else:
                        return Response({"id": 400, "message": "not enough gem"}, status=status.HTTP_400_BAD_REQUEST)

                elif league.league.base_league.playoff_count == 2:
                    if request.user.user_currency.gem >= league.league.base_league.play_off_start_gem_1:

                        request.user.user_currency.gem -= league.league.base_league.play_off_start_gem_1
                        request.user.user_currency.save()

                    else:
                        return Response({"id": 400, "message": "not enough gem"}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    if request.user.user_currency.gem >= league.league.base_league.play_off_start_gem_2:
                        request.user.user_currency.gem -= league.league.base_league.play_off_start_gem_2
                        request.user.user_currency.save()

                    else:
                        return Response({"id": 400, "message": "not enough gem"}, status=status.HTTP_400_BAD_REQUEST)

                league.play_off_count += 1
                league.play_off_status = 'start'
                league.save()

                if league.play_off_count <= 1:
                    play_off_count = league.league.base_league.play_off_start_gem

                elif league.play_off_count == 2:
                    play_off_count = league.league.base_league.play_off_start_gem_1

                else:
                    play_off_count = league.league.base_league.play_off_start_gem_2

                return Response(
                    {
                        "id": 200,
                        "message": "playoff activate",
                        "gem_count": request.user.user_currency.gem,
                        "play_off_info": {
                            "status": league.play_off_status,
                            "start_gem_price": play_off_count,
                            "unlock_need_score": league.league.base_league.play_off_unlock_score,
                            "result": [] if PlayOff.log(request.user.user_currency) == -1
                            else PlayOff.log(request.user.user_currency),
                            "num_wins": league.league.base_league.win_promoting_count
                        }
                    },
                    status=status.HTTP_200_OK
                )

            else:
                return Response({"id": 400, "message": "not enough score"}, status=status.HTTP_400_BAD_REQUEST)

        except LeagueUser.DoesNotExist as e:
            return Response(
                {
                    "id": 400,
                    "message": "user not join to league or playoff activate"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @list_route(methods=['POST'])
    def claim(self, request):
        try:
            claim = Claim.objects.get(league_player__player=request.user.user_currency, is_used=False)
            league = LeagueUser.objects.get(player=request.user.user_currency, close_league=False)
            request.user.user_currency.gem += claim.gem
            request.user.user_currency.coin += claim.coin
            claim.is_used = True
            claim.save()
            league.league_change_status = "normal"
            league.save()
            request.user.user_currency.save()
            return Response(
                {
                    'id': 200,
                    'message': 'claim success',
                    'gem': request.user.user_currency.gem,
                    'coin': request.user.user_currency.coin
                },
                status=status.HTTP_200_OK
            )

        except Claim.DoesNotExist as e:
            return Response({'id': 404, 'message': 'claim not found'}, status=status.HTTP_404_NOT_FOUND)

        except LeagueUser.DoesNotExist as e:
            return Response({'id': 404, 'message': 'league not found'}, status=status.HTTP_404_NOT_FOUND)

    @list_route(methods=['POST'])
    def skip_gem_cool_down(self, request):
        card_id = request.data.get('card_id')

        if card_id is None:
            return Response(
                {'id': 400, 'message': 'no selected card'}, status=status.HTTP_400_BAD_REQUEST)

        user_card = get_object_or_404(UserCard, user=request.user, character_id=card_id, cool_down__isnull=False)

        if request.user.user_currency.gem >= user_card.skip_cooldown_gem:
            request.user.user_currency.gem -= user_card.skip_cooldown_gem
            request.user.user_currency.save()
            user_card.cool_down = None
            user_card.save()

            return Response(
                {
                    'id': 200,
                    'message': 'skip gem success',
                    'gem': request.user.user_currency.gem,
                    'coin': request.user.user_currency.coin
                },
                status=status.HTTP_200_OK
            )

        return Response({'id': 400, 'message': 'not enough gem'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def match_count(self, request):
        profile = UserCurrency.objects.get(user=request.user)
        battle_count = profile.win_count + profile.lose_count

        if battle_count > settings.NUM_GAMES:
            battle_count = 3

        return Response(
            {
                "id": 200,
                "num_games": settings.NUM_GAMES,
                "num_played": battle_count
            },
            status=status.HTTP_200_OK
        )

    @list_route(methods=['POST'])
    def video_ads(self, request):
        try:
            valid_type = ['troop', 'chest']

            token = request.data.get('token')
            receieve_id = request.data.get('id')
            service = request.data.get('service')
            object_type = request.data.get('type')

            if object_type not in valid_type:
                raise Exception('type not valid!!!')

            video_ads = VideoAdsFactory.create(service, token)
            valid_video = video_ads.run()

            if object_type == 'troop' and valid_video:
                user_card = get_object_or_404(UserCard, user=request.user, character_id=receieve_id)

                user_card.cool_down -= timedelta(seconds=settings.SUB_COOLDOWN_TROOP)
                user_card.save()

                return Response({"id": 200, "time": user_card.cool_down_remain_time}, status=status.HTTP_200_OK)

            if object_type == 'chest' and valid_video:
                user_chest = UserChest.objects.get(user=request.user, id=receieve_id)
                user_chest.chest_opening_date -= timedelta(seconds=settings.SUB_OPENING_CHEST)
                user_chest.save()
                return Response({"id": 200, "time": user_chest.remain_time}, status=status.HTTP_200_OK)

            return Response({"id": 400, "error": "video token not valid"}, status=status.HTTP_400_BAD_REQUEST)

        except UserChest.DoesNotExist as e:
            return Response({"id": 400, "error": "chest does not exists!!!"}, status=status.HTTP_400_BAD_REQUEST)

        except UserCard.DoesNotExist as e:
            return Response({"id": 400, "error": "troop does not exists!!!"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"id": 400, "error": e.message}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def register_account(self, request):
        try:
            token = request.data.get('token')
            request.user.user_currency.google_id = request.data.get('google_id')
            request.user.user_currency.google_account = request.data.get('google_account')
            request.user.user_currency.gem += 20
            request.user.user_currency.save()

            return Response(
                {
                    "id": 200,
                    "message": "google account saved",
                    "gem": request.user.user_currency.gem
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response({"id": 400, "error": e.message}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def get_account(self, request):
        try:
            profile = get_object_or_404(UserCurrency, username=request.data.get('google_id'))

            return Response({"id": 200, "player_id": profile.user.username}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"id": 400, "error": e.message}, status=status.HTTP_400_BAD_REQUEST)


class LeagueViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = LeagueInfo.objects.all()
    serializer_class = LeagueInfoSerializer


class ShopViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    @list_route(methods=['POST'])
    def store(self, request):
        shop_item = Shop.objects.filter(store_id=request.data.get('store_id'), enable=True).first()
        serializer = self.serializer_class(shop_item)
        result = serializer.data
        result['special_offer'][0]['time_remaining'] -= int(time.mktime(datetime.now().timetuple()))
        if result['special_offer'][0]['time_remaining'] < 0:
            result['special_offer'][0]['time_remaining'] = 0
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def buy_gem(self, request):
        profile = UserCurrency.objects.get(user=request.user)
        shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

        store = (item for item in shop.gems if item['id'] == request.data.get('id')).next()

        if PurchaseLog.validate_token(request.data.get('purchase_token')):
            PurchaseLog.objects.create(user=profile, store_purchase_token=request.data.get('purchase_token'))

            return Response({'id': 404, 'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        purchase_store = FactoryStore.create(
            shop=shop,
            purchase_token=request.data.get('purchase_token'),
            product_id=request.data.get('product_id'),
            package_name=request.data.get('package_name')
        )

        is_verified, message = purchase_store.is_verified()

        if not is_verified:
            PurchaseLog.objects.create(user=profile, store_purchase_token=request.data.get('purchase_token'),
                                       store_params=message, shop=shop)
            return Response({'id': 404, 'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)

        PurchaseLog.objects.create(user=profile, store_purchase_token=request.data.get('purchase_token')
                                   , store_params=message, params=store, used_token=True, shop=shop)
        request.user.user_currency.gem += store['amount']
        request.user.user_currency.save()

        return Response({'buy_gem': store['amount'], 'user_gem': request.user.user_currency.gem},
                        status=status.HTTP_202_ACCEPTED)

    @list_route(methods=['POST'])
    def buy_coin(self, request):
        profile = UserCurrency.objects.get(user=request.user)
        shop = get_object_or_404(Shop, pk=request.data.get('shop_id'), enable=True)

        store = (item for item in shop.coins if item['id'] == request.data.get('id')).next()
        if request.user.user_currency.gem >= store['price']:
            request.user.user_currency.gem -= store['price']
            request.user.user_currency.coin += store['amount']
            request.user.user_currency.save()
            result = {
                'buy_coin': store['amount'],
                'user_coin': request.user.user_currency.coin,
                'used_gem': store['price'],
                'user_gem': request.user.user_currency.gem
            }

            CurrencyLog.objects.create(
                user=profile,
                type='GEM',
                quantity_used=store['price'],
                type_buy='COIN',
                quantity_buy=store['amount'],
                params=result
            )

            return Response(result, status=status.HTTP_202_ACCEPTED)
        return Response({'id': 400, 'message': 'gem not enough'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def buy_chest(self, request):
        profile = UserCurrency.objects.get(user=request.user)
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

            # chest = ChestGenerate(request.user, chest_type[store['type']], 'free')
            chest = CtmChestGenerate(request.user, chest_type=chest_type[store['type']])
            chest_value = chest.generate_chest()
            UserCurrency.update_currency(request.user, chest_value['gems'], chest_value['coins'])

            for unit in chest_value['units']:
                character = Unit.objects.get(moniker=unit['unit'])
                UserCard.upgrade_character(request.user, character, unit['count'])

            CurrencyLog.objects.create(
                user=profile,
                type='GEM',
                quantity_used=store['price'],
                type_buy='CHEST',
                quantity_buy=1,
                params=chest_value
            )

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
            chest = CtmChestGenerate(request.user, chest_type=chest_type[store['type']])
            chest_value = chest.generate_chest()
            UserCurrency.update_currency(request.user, chest_value['gems'], chest_value['coins'])

            for unit in chest_value['units']:
                character = Unit.objects.get(moniker=unit['unit'])
                UserCard.upgrade_character(request.user, character, unit['count'])

            chst_lst.append(chest_value)

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

        chest_gen = CtmChestGenerate(request.user, chest_type_index='chest')
        chest_gen.generate_chest()
        return Response({'message': 'chest generated'}, status=status.HTTP_200_OK)


class UserCardViewSet(DefaultsMixin, AuthMixin, viewsets.GenericViewSet):
    queryset = UserCard.objects.all()
    serializer_class = UserCardSerializer

    @list_route(methods=['POST'])
    def level_up(self, request):
        profile = UserCurrency.objects.get(user=request.user)

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
        user_card.level += 1
        user_card.save()

        serializer = UnitSerializer(user_card.character)
        data = unit_normalize_data(user_card, serializer.data)

        CurrencyLog.objects.create(
            user=profile,
            type='COIN',
            quantity_used=next_level['coins'],
            type_buy='UPDATE_UNIT',
            quantity_buy=1,
            params=data
        )

        return Response(data, status=status.HTTP_200_OK)


class UserHeroViewSet(DefaultsMixin, AuthMixin, viewsets.GenericViewSet):
    queryset = UserHero.objects.all()
    serializer_class = UserHeroSerializer

    @list_route(methods=['POST'])
    def level_up(self, request):
        profile = UserCurrency.objects.get(user=request.user)

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

        CurrencyLog.objects.create(
            user=profile,
            type='COIN',
            quantity_used=next_level['coins'],
            type_buy='UPDATE_HERO',
            quantity_buy=1,
            params=data
        )

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

        user_item.quantity -= next_level['item_cards']
        user_item.save()

        user_item.level += 1
        user_item.save()

        serializer = ItemSerializer(user_item.item)
        data = item_normalize_data(user_item, serializer.data)

        CurrencyLog.objects.create(
            user=request.user,
            type='COIN',
            quantity_used=next_level['coins'],
            type_buy='UPDATE_CARD',
            quantity_buy=1,
            params=data
        )

        return Response(data, status=status.HTTP_200_OK)


class AppConfigViewSet(viewsets.ModelViewSet):
    queryset = AppConfig.objects.all()
    serializer_class = AppConfigSerializer


class UserInboxViewSet(DefaultsMixin, AuthMixin, viewsets.GenericViewSet):
    queryset = Inbox.objects.all()
    serializer_class = InboxSerializer

    @list_route(methods=['POST'])
    def read(self, request):
        message = get_object_or_404(Inbox, user=request, id=request.data.get('id'))
        message.message_type = 'read'
        message.save()

        return Response({"id": 200, "message": "change type to read"}, status=status.HTTP_200_OK)


