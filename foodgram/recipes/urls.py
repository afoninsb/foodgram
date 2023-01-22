from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import Favorite, RecipesViewSet

router = SimpleRouter()

router.register('', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('<int:recipe_id>/favorite/', Favorite, name='favorite'),
    path('', include(router.urls)),
]
