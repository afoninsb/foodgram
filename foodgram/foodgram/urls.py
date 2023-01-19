from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('api/', include('users.urls')),
    # path('api/auth/', include('authuser.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/ingredients/', include('ingredients.urls')),
    path("admin/", admin.site.urls),
]
