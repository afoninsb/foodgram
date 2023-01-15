from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('api/users/', include('users.urls')),
    # path('api/recipes/', include('recipes.urls')),
    # path('api/tags/', include('recipes.urls')),
    # path('api/ingredients/', include('recipes.urls')),
    path("admin/", admin.site.urls),
]
