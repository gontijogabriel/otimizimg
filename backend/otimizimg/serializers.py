from rest_framework import serializers
from otimizimg.models import ImageUpload, ImageConverter

        
class ImageConverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageConverter
        fields = '__all__'
        
        
class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = '__all__'
        
        
class ImageSerializer(serializers.ModelSerializer):
    conversions = ImageConverterSerializer(many=True, read_only=True)
    
    class Meta:
        model = ImageUpload
        fields = '__all__'