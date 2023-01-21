from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes.views import Favorite, RecipesViewSet

router = SimpleRouter()

# router.register(
#     r'(?P<recipe_id>\d+)/favorite/<int:pk>', FavoriteDeleteViewSet, basename='dfavorite',
# )
# router.register(
#     r'(?P<recipe_id>\d+)/favorite', Favorite, basename='cfavorite'
# )

router.register('', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:recipe_id>/favorite/', Favorite, name='favorite')
]
