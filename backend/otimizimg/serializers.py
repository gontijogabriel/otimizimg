from rest_framework import serializers
from .models import UploadedImage, OptimizedImage, ImageRelation

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'

class OptimizedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizedImage
        fields = '__all__'

class ImageRelationSerializer(serializers.ModelSerializer):
    original_image = UploadedImageSerializer()
    optimized_image = OptimizedImageSerializer()

    class Meta:
        model = ImageRelation
        fields = '__all__'

class OptimizeImageSerializer(serializers.Serializer):
    optimized_format = serializers.ChoiceField(choices=OptimizedImage.SUPPORTED_FORMATS, default='JPEG')
    quality = serializers.IntegerField(min_value=1, max_value=100, default=85)