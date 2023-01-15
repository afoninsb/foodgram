from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UsersViewSet, get_token, signup

router = SimpleRouter()

router.register('users', UsersViewSet, basename='users')

auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('', include(router.urls)),
]
