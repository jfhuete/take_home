from django.urls import path, include
from rest_framework import routers

from movies.views import MovieViewSet, PerformancesViewSet

router = routers.DefaultRouter()

router.register(r'movies', MovieViewSet)
router.register(r'performances', PerformancesViewSet,  basename='Perfomance')

urlpatterns = [
    path('', include(router.urls)),
]
