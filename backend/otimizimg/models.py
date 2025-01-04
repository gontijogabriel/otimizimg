from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
import os

def validate_image(value):
    try:
        image = PILImage.open(value)
        image.verify()  # Verifica se a imagem é válida
        if image.format.upper() not in ['JPEG', 'PNG', 'WEBP']:
            raise ValidationError('Formato não suportado. Use JPEG, PNG ou WebP.')
    except Exception:
        raise ValidationError('Arquivo inválido. Por favor, envie uma imagem válida.')

class UploadedImage(models.Model):
    SUPPORTED_FORMATS = [
        ('JPEG', 'JPEG'),
        ('PNG', 'PNG'),
        ('WEBP', 'WebP'),
    ]

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
    optimized_image = models.ImageField(
        upload_to='optimized/',
        null=True,
        blank=True,
        help_text='Versão otimizada da imagem'
    )
    optimized_format = models.CharField(
        max_length=10,
        choices=SUPPORTED_FORMATS,
        null=True,
        blank=True,
        help_text='Formato da imagem otimizada'
    )
    optimized_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Tamanho otimizado em bytes'
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
        verbose_name = 'Imagem'
        verbose_name_plural = 'Imagens'

    def __str__(self):
        return f'Imagem {self.id} - {self.get_dimensions()}'

    def get_dimensions(self):
        return f'{self.width}x{self.height}'

    def save(self, *args, **kwargs):
        # Se é um novo objeto ou a imagem original mudou
        if not self.pk or 'original_image' in self.__dict__:
            with PILImage.open(self.original_image) as img:
                # Salva informações da imagem original
                self.original_format = img.format
                self.width = img.width
                self.height = img.height
                self.original_size = self.original_image.size

        # Limpa otimização anterior se a imagem original mudou
        if 'original_image' in self.__dict__:
            if self.optimized_image:
                try:
                    old_path = self.optimized_image.path
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass
            self.optimized_image = None
            self.optimized_format = None
            self.optimized_size = None

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Remove os arquivos ao deletar o objeto
        try:
            if self.original_image:
                if os.path.exists(self.original_image.path):
                    os.remove(self.original_image.path)
            if self.optimized_image:
                if os.path.exists(self.optimized_image.path):
                    os.remove(self.optimized_image.path)
        except Exception:
            pass
        super().delete(*args, **kwargs)