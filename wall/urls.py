from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from django.conf.urls import url, include
from django.contrib import admin

from wall.views import (
    PostViewSet, LikeViewSet, NotificationViewSet, ObtainAuthToken
)

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^api/auth/', ObtainAuthToken.as_view()),
    url(r'^admin/', admin.site.urls),
]
