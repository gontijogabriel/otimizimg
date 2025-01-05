from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from otimizimg.models import ImageUpload, ImageConverter
from otimizimg.serializers import ImageUploadSerializer, ImageConverterSerializer, ImageSerializer

from django.conf import settings

import os
from PIL import Image
from PIL.ExifTags import TAGS as ExifTags


class ImageView(viewsets.ModelViewSet):
    queryset = ImageUpload.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ImageSerializer
        return ImageUploadSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        image_instance = serializer.instance
        image_path = image_instance.url.path

        with Image.open(image_path) as img:
            image_instance.filename = img.filename
            image_instance.format = img.format
            image_instance.width = img.width
            image_instance.height = img.height
            image_instance.color_mode = img.mode
            image_instance.file_size = os.path.getsize(image_path)
            image_instance.dpi = str(img.info.get('dpi', ''))
            
            exif_data = img._getexif()
            if exif_data:
                exif_details = {}
                for tag, value in exif_data.items():
                    tag_name = ExifTags.get(tag, tag)
                    exif_details[tag_name] = value
                image_instance.metadata = exif_details
                
        image_instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'])
    def convert(self, request, *args, **kwargs):
        image_id = request.data.get('image_id')
        new_format = request.data.get('new_format', 'JPEG').upper()
        
        if not image_id:
            raise ValidationError({'image_id': 'This field is required.'})
            
        try:
            original_image = ImageUpload.objects.get(id=image_id)
        except ImageUpload.DoesNotExist:
            raise ValidationError({'image_id': 'Image not found.'})

        with Image.open(original_image.url.path) as img:
            original_filename = os.path.splitext(os.path.basename(original_image.filename))[0] if original_image.filename else os.path.splitext(os.path.basename(original_image.url.name))[0]
            new_filename = f"convert_{original_filename}.{new_format.lower()}"
            
            if img.mode in ('RGBA', 'LA') and new_format in ('JPEG', 'JPG'):
                img = img.convert('RGB')
            
            convert_dir = os.path.join(settings.MEDIA_ROOT, 'convert')
            os.makedirs(convert_dir, exist_ok=True)
            
            temp_path = os.path.join(convert_dir, new_filename)
            img.save(temp_path, format=new_format)
            
            converter_instance = ImageConverter.objects.create(
                original_file=original_image,
                filename=new_filename,
                format=new_format,
                width=img.width,
                height=img.height,
                color_mode=img.mode,
                file_size=os.path.getsize(temp_path),
                dpi=str(img.info.get('dpi', '')),
                metadata=str(img.info)
            )
            
            with open(temp_path, 'rb') as temp_file:
                converter_instance.url.save(new_filename, temp_file, save=True)
            
            os.remove(temp_path)
            
            serializer = ImageConverterSerializer(converter_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
