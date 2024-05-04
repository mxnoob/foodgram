from django.urls import path, include

from .users.urls import user_router

app_name = 'api'

urlpatterns = [
    path('', include('api.recipes.urls')),
    path('', include(user_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
