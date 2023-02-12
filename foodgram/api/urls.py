from django.urls import include, path
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.routers import SimpleRouter

from api.views.ingredients import IngredientsViewSet
from api.views.recipes import RecipesViewSet
from api.views.tags import TagsViewSet
from api.views.users import UsersViewSet

app_name = 'api'

router = SimpleRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagsViewSet, basename='tags')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/set_password/',
        DjoserUserViewSet.as_view({'post': 'set_password'})
    ),
    path(
        'users/me/',
        DjoserUserViewSet.as_view({'get': 'me'})
    ),
    path('', include(router.urls)),
]
