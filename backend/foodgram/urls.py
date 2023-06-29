from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns = [
    path('', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    # path('auth/', include('users.urls')),
    # path('auth/', include('django.contrib.auth.urls')),
    # path('about/', include('about.urls', namespace='about')),
    # path('api-auth/', include('rest_framework.urls')),
]