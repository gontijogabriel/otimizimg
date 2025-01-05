from rest_framework.routers import DefaultRouter
from django.urls import path, include
from otimizimg.views import ImageView


router = DefaultRouter()
router.register(r'image', ImageView)

urlpatterns = [
    path('', include(router.urls)),
]