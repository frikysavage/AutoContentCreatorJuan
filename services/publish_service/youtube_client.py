import logging
from shared.config.settings import settings

logger = logging.getLogger(__name__)

def upload_to_youtube(video_path: str, titulo: str, descripcion: str, synthetic_content: bool) -> str:
    """
    Mocks uploading a video to YouTube as 'unlisted'.
    In a real scenario, this would use google-auth and google-api-python-client,
    build the youtube v3 service, and upload the video file with the specified
    metadata, making sure to flag synthetic_content if required by API schema.
    Returns the video_id.
    """
    logger.info(f"Uploading {video_path} to YouTube. Title: {titulo}")
    if synthetic_content:
        logger.info("Flagging as synthetic content.")
    
    # Mock video ID
    return "mock_video_id_123"

def set_video_public(video_id: str):
    """
    Mocks updating the video status from 'unlisted' to 'public'.
    """
    logger.info(f"Setting video {video_id} to public.")
