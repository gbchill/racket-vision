import os
import tempfile
from pathlib import Path
import uuid
import logging
from fastapi import UploadFile

from .supabase_client import supabase, VIDEOS_BUCKET

#set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def save_upload_file(upload_file: UploadFile) -> str:
    """
    Save the uploaded file to a temporary location
    Returns the path to the saved file
    """
    try:
        #create a temporary file
        suffix = Path(upload_file.filename).suffix
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            #write the uploaded file to the temporary file
            content = await upload_file.read()
            temp_file.write(content)
            logger.info(f"Saved uploaded file to temporary location: {temp_file.name}")
            return temp_file.name
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}", exc_info=True)
        raise

def upload_to_supabase(file_path: str, file_type: str) -> str:
    """
    Upload a file to Supabase storage
    Returns the public URL of the uploaded file
    """
    try:
        #generate a unique filename
        filename = f"{uuid.uuid4()}{Path(file_path).suffix}"
        logger.info(f"Uploading {file_type} file to Supabase: {filename}")
        
        #try to create the bucket if it fails, it probably already exists
        try:
            logger.info(f"Creating bucket (if it doesn't exist): {VIDEOS_BUCKET}")
            supabase.storage.create_bucket(VIDEOS_BUCKET, {'public': True})
            logger.info(f"Bucket created: {VIDEOS_BUCKET}")
        except Exception as e:
            logger.info(f"Note: {e}")
            logger.info(f"If the bucket already exists, this is expected and not an error")
        
        #upload the file
        file_size = os.path.getsize(file_path)
        logger.info(f"File size: {file_size} bytes")
        
        file_content = None
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        #determine the content type
        content_type = f"video/{Path(file_path).suffix.lstrip('.')}"
        logger.info(f"Content type: {content_type}")
            
        #upload using the correct API
        path = f"{file_type}/{filename}"
        logger.info(f"Uploading to path: {path}")
        
        res = supabase.storage.from_(VIDEOS_BUCKET).upload(
            path=path,
            file=file_content,
            file_options={"content-type": content_type}
        )
        logger.info(f"Upload response: {res}")
        
        # Get the public URL
        url = supabase.storage.from_(VIDEOS_BUCKET).get_public_url(path)
        logger.info(f"Public URL: {url}")
        
        return url
    except Exception as e:
        logger.error(f"Error uploading to Supabase: {str(e)}", exc_info=True)
        raise

def cleanup_temp_files(files):
    """Remove temporary files"""
    for file in files:
        try:
            if file and os.path.exists(file):
                os.unlink(file)
                logger.info(f"Removed temporary file: {file}")
        except Exception as e:
            logger.error(f"Error removing temporary file {file}: {str(e)}")