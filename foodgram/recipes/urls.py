from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import RecipesViewSet

router = SimpleRouter()

router.register('', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
