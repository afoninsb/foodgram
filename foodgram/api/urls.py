from django.urls import include, path
from api.views.ingredients import IngredientsViewSet
from api.views.recipes import RecipesViewSet
from rest_framework.routers import SimpleRouter
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
    path('', include(router.urls)),
]
