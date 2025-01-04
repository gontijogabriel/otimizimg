from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from .models import UploadedImage, OptimizedImage, ImageRelation
from .serializers import UploadedImageSerializer, OptimizedImageSerializer, ImageRelationSerializer, OptimizeImageSerializer
from .utils import optimize_image

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        uploaded_image = self.get_object()  # Obtém a imagem original
        serializer = OptimizeImageSerializer(data=request.data)
        
        if serializer.is_valid():
            optimized_format = serializer.validated_data['optimized_format']
            quality = serializer.validated_data['quality']

            # Otimiza a imagem
            optimized_io, optimized_size = optimize_image(uploaded_image.original_image.path, optimized_format, quality)

            # Converte BytesIO para InMemoryUploadedFile
            optimized_file = InMemoryUploadedFile(
                optimized_io, None, uploaded_image.original_image.name, 
                "image/" + optimized_format.lower(), optimized_size, None
            )

            # Cria a imagem otimizada
            optimized_image = OptimizedImage.objects.create(
                optimized_image=optimized_file,
                optimized_format=optimized_format,
                optimized_size=optimized_size,
                width=uploaded_image.width,
                height=uploaded_image.height
            )

            # Cria a relação entre a imagem original e a otimizada
            ImageRelation.objects.create(
                original_image=uploaded_image,
                optimized_image=optimized_image
            )

            return Response({
                'status': 'imagem otimizada com sucesso',
                'optimized_image': OptimizedImageSerializer(optimized_image).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OptimizedImageViewSet(viewsets.ModelViewSet):
    queryset = OptimizedImage.objects.all()
    serializer_class = OptimizedImageSerializer

class ImageRelationViewSet(viewsets.ModelViewSet):
    queryset = ImageRelation.objects.all()
    serializer_class = ImageRelationSerializer