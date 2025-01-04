from django.db import models
from PIL import Image as PILImage
import os

from otimizimg.validators import validate_image

class UploadedImage(models.Model):
    original_image = models.ImageField(
        upload_to='originals/',
        validators=[validate_image],
        help_text='Imagem original para otimização'
    )
    original_format = models.CharField(
        max_length=10,
        editable=False,
        help_text='Formato original da imagem'
    )
    original_size = models.PositiveIntegerField(
        editable=False,
        help_text='Tamanho original em bytes'
    )
    width = models.IntegerField(
        default=0,
        editable=False,
        help_text='Largura da imagem em pixels'
    )
    height = models.IntegerField(
        default=0,
        editable=False,
        help_text='Altura da imagem em pixels'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora do upload'
    )
    last_modified = models.DateTimeField(
        auto_now=True,
        help_text='Última modificação'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Imagem Original'
        verbose_name_plural = 'Imagens Originais'

    def __str__(self):
        return f'Imagem Original {self.id} - {self.get_dimensions()}'

    def get_dimensions(self):
        return f'{self.width}x{self.height}'

    def save(self, *args, **kwargs):
        if not self.pk or 'original_image' in self.__dict__:
            with PILImage.open(self.original_image) as img:
                self.original_format = img.format
                self.width = img.width
                self.height = img.height
                self.original_size = self.original_image.size

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            if self.original_image:
                if os.path.exists(self.original_image.path):
                    os.remove(self.original_image.path)
        except Exception:
            pass
        super().delete(*args, **kwargs)


class OptimizedImage(models.Model):
    SUPPORTED_FORMATS = [
        ('JPEG', 'JPEG'),
        ('PNG', 'PNG'),
        ('WEBP', 'WebP'),
    ]

    optimized_image = models.ImageField(
        upload_to='optimized/',
        validators=[validate_image],
        help_text='Versão otimizada da imagem'
    )
    optimized_format = models.CharField(
        max_length=10,
        choices=SUPPORTED_FORMATS,
        help_text='Formato da imagem otimizada'
    )
    optimized_size = models.PositiveIntegerField(
        help_text='Tamanho otimizado em bytes'
    )
    width = models.IntegerField(
        default=0,
        editable=False,
        help_text='Largura da imagem otimizada em pixels'
    )
    height = models.IntegerField(
        default=0,
        editable=False,
        help_text='Altura da imagem otimizada em pixels'
    )

    class Meta:
        verbose_name = 'Imagem Otimizada'
        verbose_name_plural = 'Imagens Otimizadas'

    def __str__(self):
        return f'Imagem Otimizada {self.id} - {self.get_dimensions()}'

    def get_dimensions(self):
        return f'{self.width}x{self.height}'

    def save(self, *args, **kwargs):
        if not self.pk or 'optimized_image' in self.__dict__:
            with PILImage.open(self.optimized_image) as img:
                self.optimized_format = img.format
                self.width = img.width
                self.height = img.height
                self.optimized_size = self.optimized_image.size

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            if self.optimized_image:
                if os.path.exists(self.optimized_image.path):
                    os.remove(self.optimized_image.path)
        except Exception:
            pass
        super().delete(*args, **kwargs)


class ImageRelation(models.Model):
    original_image = models.OneToOneField(
        UploadedImage,
        on_delete=models.CASCADE,
        related_name='optimized_relation',
        help_text='Imagem original'
    )
    optimized_image = models.OneToOneField(
        OptimizedImage,
        on_delete=models.CASCADE,
        related_name='original_relation',
        help_text='Imagem otimizada'
    )
    related_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Data e hora da relação'
    )

    class Meta:
        verbose_name = 'Relação de Imagem'
        verbose_name_plural = 'Relações de Imagem'

    def __str__(self):
        return f'Relação {self.id} - Original: {self.original_image.id}, Otimizada: {self.optimized_image.id}'