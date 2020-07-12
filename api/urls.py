from django.urls import include, path
from rest_framework import routers

from .views import BoardViewSet

router = routers.DefaultRouter()
router.register(r'boards', BoardViewSet, basename='boards')

urlpatterns = [
    path('v1/', include(router.urls)),
]
