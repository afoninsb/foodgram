from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import GetSubscriptionsViewSet, UsersViewSet


router = SimpleRouter()

router.register('users/subscriptions',
                GetSubscriptionsViewSet, basename='get_subscriptions')
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    # path('users/<int:id>/subscribe/', Subscribe, name='subscribe'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
