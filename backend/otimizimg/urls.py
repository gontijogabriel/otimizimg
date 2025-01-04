from django.urls import path, include
from rest_framework.routers import DefaultRouter
from otimizimg.views import UploadedImageViewSet

router = DefaultRouter()
router.register(r'images', UploadedImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
