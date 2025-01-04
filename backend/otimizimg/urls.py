from rest_framework.routers import DefaultRouter
from django.urls import path, include
from otimizimg.views import UploadedImageViewSet, OptimizedImageViewSet, ImageRelationViewSet


router = DefaultRouter()
router.register(r'uploaded-images', UploadedImageViewSet)
router.register(r'optimized-images', OptimizedImageViewSet)
router.register(r'image-relations', ImageRelationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]