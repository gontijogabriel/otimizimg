from PIL import Image as PILImage
import io

def optimize_image(image_path, optimized_format='JPEG', quality=85):
    with PILImage.open(image_path) as img:
        img = img.convert('RGB')  # Converte para RGB se necessário
        optimized_io = io.BytesIO()
        img.save(optimized_io, format=optimized_format, quality=quality)
        optimized_io.seek(0)
        return optimized_io, optimized_io.tell()