import os
from django.conf import settings
from PIL import Image
import io
import uuid
from django.core.files.base import ContentFile

def compress_image(image_field, size=(800,800), quality=85):
    # Open the image
    # Convert to RGB if it's a PNG - якщо зображення PNG, перетворити на RGB
    image = Image.open(image_field).convert('RGB')

    # Зберігаємо оригінальне зображення його пропорції aspect ratio
    image.thumbnail(size, Image.LANCZOS)

    # робимо ім'я нового зображення
    uid = str(uuid.uuid4())[:10]
    image_name=f'{uid}.webp'

    # зберігаємо зображення в пам'яті
    output = io.BytesIO()

    image.save(output, format='WEBP', quality=quality)

    output.seek(0)

    # зберігаємо зображення в моделі
    optimized_image = ContentFile(output.getvalue())

    # повертаємо оптимізоване зображення та ім'я файлу
    return optimized_image, image_name

def save_custom_image(image, size, folder):
    optimized_image, image_name = compress_image(image, size)
    path = os.path.join(folder,image_name)
    full_path = os.path.join(settings.IMAGES_ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(optimized_image.read())
    return image_name