from django.urls import include, path
from rest_framework.routers import SimpleRouter

from ingredients.views import IngredientsViewSet

router = SimpleRouter()

router.register('', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
