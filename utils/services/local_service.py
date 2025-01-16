import os
from django.conf import settings
from uuid import uuid4

def save_file_to_media(file):
    """
    Save a file to the media folder in a Django project.
    """
    try:
        # Validate file type
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            raise Exception(f"Format not supported: {file.content_type}")

        # Validate file size (max 7MB)
        max_size = 7 * 1024 * 1024
        if file.size > max_size:
            raise Exception(f"File too large: {file.size / (1024 * 1024):.2f} MB (max: 7 MB)")

        # Create a unique file name
        file_name = f"{uuid4().hex}_{file.name}"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Save file to the media folder
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Return the media URL
        return f"{settings.MEDIA_URL}{file_name}"

    except Exception as e:
        raise Exception(f"Save to media error: {str(e)}")
