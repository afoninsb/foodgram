from django.urls import include, path
from rest_framework.routers import SimpleRouter

from tags.views import TagsViewSet

router = SimpleRouter()

router.register('', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
