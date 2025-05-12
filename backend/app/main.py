import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import logging
import traceback
import tempfile

from .mediapipe_processor import process_video
from .video import save_upload_file, upload_to_supabase, cleanup_temp_files

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the temporary directory for storing videos
TEMP_DIR = tempfile.gettempdir()

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route for serving video files
@app.get("/api/video/{filename}")
async def get_video(filename: str):
    """Serve video files from the temporary directory"""
    file_path = os.path.join(TEMP_DIR, filename)
    logger.info(f"Requested video file: {file_path}")
    
    if not os.path.exists(file_path):
        logger.error(f"Video file not found: {file_path}")
        raise HTTPException(status_code=404, detail="Video not found")
    
    return FileResponse(file_path, media_type="video/mp4")

@app.get("/")
def read_root():
    return {"message": "RacketVision API"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    """
    Upload a video, process it with MediaPipe, and store both videos in Supabase
    Returns the URLs to the original and processed videos
    """
    logger.info(f"Received upload request for file: {file.filename}")
    
    # Validate file type
    if not file.filename.lower().endswith(('.mp4', '.mov', '.avi', '.webm')):
        logger.warning(f"Invalid file type: {file.filename}")
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a video file.")
    
    temp_files = []
    processed_url = None
    original_url = None
    processed_path = None
    temp_path = None
    
    try:
        # Save the uploaded file
        logger.info("Saving uploaded file")
        temp_path = await save_upload_file(file)
        temp_files.append(temp_path)
        logger.info(f"Saved uploaded file to: {temp_path}")
        
        # Process the video with MediaPipe
        logger.info("Processing video with MediaPipe")
        try:
            processed_path = process_video(temp_path)
            temp_files.append(processed_path)
            logger.info(f"Processed video saved to: {processed_path}")
        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")
        
        # Upload both videos to Supabase
        logger.info("Uploading videos to Supabase")
        try:
            # Check if environment variables are set
            if not os.environ.get("SUPABASE_URL") or not os.environ.get("SUPABASE_KEY"):
                logger.error("Supabase environment variables not set")
                logger.info("Using local file paths for testing")
                
                # Use local paths for testing
                original_url = f"http://localhost:8000/api/video/{os.path.basename(temp_path)}"
                processed_url = f"http://localhost:8000/api/video/{os.path.basename(processed_path)}"
            else:
                # Try uploading to Supabase
                try:
                    original_url = upload_to_supabase(temp_path, "original")
                    logger.info(f"Original URL: {original_url}")
                except Exception as e:
                    logger.error(f"Error uploading original video: {str(e)}")
                    # Fallback to local URL
                    original_url = f"http://localhost:8000/api/video/{os.path.basename(temp_path)}"
                    
                try:
                    processed_url = upload_to_supabase(processed_path, "processed")
                    logger.info(f"Processed URL: {processed_url}")
                except Exception as e:
                    logger.error(f"Error uploading processed video: {str(e)}")
                    # Fallback to local URL
                    processed_url = f"http://localhost:8000/api/video/{os.path.basename(processed_path)}"
                
        except Exception as e:
            logger.error(f"Error with Supabase upload: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Use local file paths
            if processed_path and temp_path:
                processed_url = f"http://localhost:8000/api/video/{os.path.basename(processed_path)}"
                original_url = f"http://localhost:8000/api/video/{os.path.basename(temp_path)}"
            else:
                raise HTTPException(status_code=500, detail=f"Error uploading videos: {str(e)}")
        
        # Return the URLs
        return JSONResponse({
            "original_url": original_url,
            "processed_url": processed_url,
            "message": "Video processed successfully"
        })
    
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Try to return something useful for debugging
        response = {
            "detail": f"Error processing video: {str(e)}",
            "message": "Failed to process video"
        }
        
        # If we got to the point of having processed videos, include their paths
        if processed_path and temp_path:
            response["processed_url"] = f"http://localhost:8000/api/video/{os.path.basename(processed_path)}"
            response["original_url"] = f"http://localhost:8000/api/video/{os.path.basename(temp_path)}"
            
        return JSONResponse(status_code=500, content=response)
    
    finally:
        # For debugging, don't clean up files immediately
        # This allows us to access them through the /api/video endpoint
        logger.info(f"Keeping temporary files for serving: {temp_files}")
        # In production, you'd want to clean these up after a certain time
        # cleanup_temp_files(temp_files)