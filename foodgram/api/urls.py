from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ingredients.views import IngredientsViewSet
from recipes.views import RecipesViewSet
from tags.views import TagsViewSet
from users.views import UsersViewSet
# from users.views import GetSubscriptionsViewSet, UsersViewSet

app_name = 'api'

router = SimpleRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')
# router.register('users/subscriptions',
#                 GetSubscriptionsViewSet, basename='get_subscriptions')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
