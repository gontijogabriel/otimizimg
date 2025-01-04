import os
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from PIL import Image as PILImage
from otimizimg.models import UploadedImage
from otimizimg.serializers import UploadedImageSerializer

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadedImage.objects.all()
    serializer_class = UploadedImageSerializer

    @action(detail=True, methods=['post'])
    def optimize(self, request, pk=None):
        try:
            image = self.get_object()
            format = request.data.get('format', 'JPEG')
            
            # Validação do formato
            if format not in dict(UploadedImage.SUPPORTED_FORMATS):
                return Response(
                    {'error': 'Formato não suportado'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validação da qualidade
            quality = request.data.get('quality', 85)
            try:
                quality = int(quality)
                if not (1 <= quality <= 100):
                    raise ValueError()
            except (TypeError, ValueError):
                return Response(
                    {'error': 'Qualidade deve ser um número entre 1 e 100'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Cria diretório se não existir
            output_dir = os.path.join(settings.MEDIA_ROOT, 'optimized')
            os.makedirs(output_dir, exist_ok=True)

            # Define caminho do arquivo otimizado
            output_filename = f'{image.id}_{format.lower()}'
            if format.upper() == 'JPEG':
                output_filename += '.jpg'
            else:
                output_filename += f'.{format.lower()}'
            
            output_path = os.path.join(output_dir, output_filename)
            relative_path = os.path.join('optimized', output_filename)

            # Otimiza a imagem
            with PILImage.open(image.original_image.path) as img:
                # Converte para RGB se necessário
                if format.upper() == 'JPEG' and img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Salva a imagem otimizada
                img.save(
                    output_path,
                    format=format,
                    quality=quality,
                    optimize=True
                )

            # Atualiza o modelo
            if image.optimized_image:
                try:
                    old_path = image.optimized_image.path
                    if os.path.exists(old_path) and old_path != output_path:
                        os.remove(old_path)
                except Exception:
                    pass

            image.optimized_image = relative_path
            image.optimized_format = format
            image.optimized_size = os.path.getsize(output_path)
            image.save()

            return Response(UploadedImageSerializer(image).data)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )