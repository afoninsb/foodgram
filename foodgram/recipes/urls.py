from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import FavoriteViewSet, RecipesViewSet

router = SimpleRouter()

router.register(
    r'(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorite'
)

router.register('', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
