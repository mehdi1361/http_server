from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LeagueViewSet, \
    ShopViewSet, UserCardViewSet, UserHeroViewSet, UserItemViewset, UserChestViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
# router.register(r'box', BenefitViewSet) # BEnefitViewSet with filter coin and gem type
router.register(r'league', LeagueViewSet)
router.register(r'shop', ShopViewSet)
router.register(r'troop', UserCardViewSet)
router.register(r'hero', UserHeroViewSet)
router.register(r'item', UserItemViewset)
router.register(r'chest', UserChestViewSet)



