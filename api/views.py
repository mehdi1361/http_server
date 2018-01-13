from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, BenefitSerializer, LeagueInfoSerializer, ShopSerializer, UserChestSerializer
from objects.models import BenefitBox, UserBuy, UserCurrency, Hero, UserHero, LeagueInfo, UserChest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from shopping.models import Shop
from django.conf import  settings

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
            {'id': 200, 'message': 'ok'}, status=status.HTTP_400_BAD_REQUEST)

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

        chest.chest_opening_date = datetime.now() + timedelta(hours=5)
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
    def open_chest(self, request):
        chest = get_object_or_404(UserChest, pk=request.data.get('id'), user=request.user, status='ready')


class BenefitViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BenefitBox.objects.all()
    serializer_class = BenefitSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('box', )

    @list_route(methods=['POST'])
    def buy(self, request):
        benefit = get_object_or_404(BenefitBox, pk=request.data.get('id'))
        UserBuy.objects.create(user=request.user, benefit=benefit)
        chest, created = UserCurrency.objects.get_or_create(defaults={'user': request.user})

        if benefit.box == 'GEM':
            chest.gem += benefit.quantity

        if benefit.box == 'COIN':
            chest.coin += benefit.quantity

        chest.save()

        return Response({'id': 201, 'message': 'buy request created'}, status=status.HTTP_202_ACCEPTED)
        # TODO check payment validation


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


class UserChestViewSet(DefaultsMixin, AuthMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = UserChest.objects.all()
    serializer_class = UserChestSerializer

    @list_route(methods=['POST'])
    def generate_win_chest(self, request):
        if not UserChest.deck_is_open(request.user):
            return Response({'message': 'deck is full'}, status=status.HTTP_406_NOT_ACCEPTABLE)


