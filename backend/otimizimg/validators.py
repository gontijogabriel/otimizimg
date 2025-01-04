from django.core.exceptions import ValidationError
from PIL import Image as PILImage

def validate_image(value):
    try:
        image = PILImage.open(value)
        image.verify()  # Verifica se a imagem é válida
        if image.format.upper() not in ['JPEG', 'PNG', 'WEBP']:
            raise ValidationError('Formato não suportado. Use JPEG, PNG ou WebP.')
    except Exception:
        raise ValidationError('Arquivo inválido. Por favor, envie uma imagem válida.')