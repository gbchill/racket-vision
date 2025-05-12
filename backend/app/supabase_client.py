import os
import logging
from dotenv import load_dotenv
from supabase import create_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Define bucket name
VIDEOS_BUCKET = "tennis-videos"

# Check if credentials are available
if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("Supabase credentials not found in environment variables")
    logger.warning("Make sure you have created a .env file with SUPABASE_URL and SUPABASE_KEY")
else:
    # Mask credentials for security in logs
    logger.info(f"Supabase URL: {SUPABASE_URL[:10]}... (truncated for security)")
    logger.info(f"Supabase Key: {SUPABASE_KEY[:5]}... (truncated for security)")

# Initialize Supabase client
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Supabase client initialized successfully")
    
    # Test the connection
    try:
        # Simple test to verify the connection is working
        buckets = supabase.storage.list_buckets()
        logger.info(f"Supabase connection successful. Found {len(buckets)} buckets.")
        
        # Try to create the bucket right away
        try:
            supabase.storage.create_bucket(VIDEOS_BUCKET, {'public': True})
            logger.info(f"Created bucket: {VIDEOS_BUCKET}")
        except Exception as e:
            # If this fails, the bucket might already exist, which is fine
            logger.info(f"Note: {str(e)}")
            logger.info(f"If the bucket already exists, this is expected and not an error")
    except Exception as e:
        logger.error(f"Error testing Supabase connection: {str(e)}")
        
except Exception as e:
    logger.error(f"Error initializing Supabase client: {str(e)}")
    # Don't crash immediately - create a placeholder that will raise exceptions when used
    supabase = None

logger.info(f"Using Supabase bucket: {VIDEOS_BUCKET}")