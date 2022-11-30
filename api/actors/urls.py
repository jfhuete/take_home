from django.urls import path, include
from rest_framework import routers

from actors.views import ActorViewSet, CommonActorsViewSet

router = routers.DefaultRouter()

router.register(r'actors', ActorViewSet)
router.register(r'common_actors', CommonActorsViewSet,  basename='CommondAct')

urlpatterns = [
    path('', include(router.urls)),
]
