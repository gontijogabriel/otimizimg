from rest_framework import serializers
from otimizimg.models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'
        read_only_fields = ('original_format', 'original_size', 'width', 'height', 
                          'optimized_format', 'optimized_size', 'uploaded_at', 'last_modified')