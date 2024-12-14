from supabase import create_client
import os
import uuid
from urllib.parse import urlparse, unquote


SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_BUCKET_ROOMS = os.getenv('SUPABASE_BUCKET_ROOMS')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_single_image(file):
    """
    Upload a single file to Supabase and return its public URL
    """
    try:
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            raise Exception(f"Format not supported : {file.content_type}")

        max_size = 7 * 1024 * 1024
        if file.size > max_size:
            raise Exception(f"File too large : {file.size / (1024 * 1024):.2f} Mo (max : 7 Mo)")

        file_name = f"Room_images/{uuid.uuid4().hex}_{file.name}"

        response = supabase.storage.from_(SUPABASE_BUCKET_ROOMS).upload(file_name, file.read())
        if hasattr(response, 'error') and response.error:
            raise Exception(response["error"]["message"])

        public_url = supabase.storage.from_(SUPABASE_BUCKET_ROOMS).get_public_url(file_name)

        return public_url

    except Exception as e:
        raise Exception(f"Upload error : {str(e)}")

def upload_multiple_images(files):
    """
    Upload multiple files to Supabase and return a list of public URLs.
    """
    urls = []
    try:
        for file in files:
            url = upload_single_image(file)
            urls.append(url)
        return urls
    except Exception as e:
        raise Exception(f"Upload multiple error : {str(e)}")

def upload_images(files):
    """
    Detects if the upload is for a single image or multiple and manages accordingly.
    """
    if isinstance(files, list):
        return upload_multiple_images(files)
    else:
        return [upload_single_image(files)]

def remove_file(url):
    """
    Remove a file from Supabase storage using its public URL.
    """
    try:
        bucket_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET_ROOMS}/"
        if not url.startswith(bucket_url):
            raise Exception("Invalid URL: Not a Supabase storage public URL")

        parsed_url = urlparse(url)
        clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        file_path = unquote(clean_url.replace(bucket_url, ""))

        response = supabase.storage.from_(SUPABASE_BUCKET_ROOMS).remove([file_path])

        if hasattr(response, 'error') and response.error:
            raise Exception(response["error"]["message"])

        return {"success": True, "message": "File removed successfully"}
    except Exception as e:
        raise Exception(f"Remove error: {str(e)}")