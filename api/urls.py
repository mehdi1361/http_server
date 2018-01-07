from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BenefitViewSet, LeagueViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'box', BenefitViewSet) # BEnefitViewSet with filter coin and gem type
router.register(r'league', LeagueViewSet)


