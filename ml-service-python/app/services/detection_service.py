from fastapi import UploadFile, HTTPException
from typing import Dict, Any
import logging
from ..models.image_detector import ImageDeepfakeDetector
from ..models.audio_detector import AudioDeepfakeDetector
from ..models.video_detector import VideoDeepfakeDetector
from ..utils.file_handler import FileHandler

logger = logging.getLogger(__name__)

class DetectionService:
    def __init__(self):
        self.image_detector = ImageDeepfakeDetector()
        self.audio_detector = AudioDeepfakeDetector()
        self.video_detector = VideoDeepfakeDetector()
        self.file_handler = FileHandler()
        logger.info("Detection service initialized")
    
    async def detect_image(self, file: UploadFile) -> Dict[str, Any]:
        """Detect deepfake in image"""
        file_path = None
        try:
            # Validate file
            self._validate_image_file(file)
            
            # Save uploaded file
            file_path = await self.file_handler.save_upload_file(file, suffix='.jpg')
            
            # Get file info
            file_info = self.file_handler.get_file_info(file)
            
            # Detect deepfake
            result = self.image_detector.predict(file_path)
            
            # Add file metadata
            result.update({
                "file_name": file_info["filename"],
                "file_size": file_info["size"] or len(await file.read()),
                "content_type": file_info["content_type"]
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Image detection failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if file_path:
                self.file_handler.cleanup_file(file_path)
    
    async def detect_audio(self, file: UploadFile) -> Dict[str, Any]:
        """Detect deepfake in audio"""
        file_path = None
        try:
            # Validate file
            self._validate_audio_file(file)
            
            # Save uploaded file
            file_path = await self.file_handler.save_upload_file(file, suffix='.wav')
            
            # Get file info
            file_info = self.file_handler.get_file_info(file)
            
            # Detect deepfake
            result = self.audio_detector.predict(file_path)
            
            # Add file metadata
            result.update({
                "file_name": file_info["filename"],
                "file_size": file_info["size"] or len(await file.read()),
                "content_type": file_info["content_type"]
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Audio detection failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if file_path:
                self.file_handler.cleanup_file(file_path)
    
    async def detect_video(self, file: UploadFile) -> Dict[str, Any]:
        """Detect deepfake in video"""
        file_path = None
        try:
            # Validate file
            self._validate_video_file(file)
            
            # Save uploaded file  
            file_path = await self.file_handler.save_upload_file(file, suffix='.mp4')
            
            # Get file info
            file_info = self.file_handler.get_file_info(file)
            
            # Detect deepfake
            result = self.video_detector.predict(file_path)
            
            # Add file metadata
            result.update({
                "file_name": file_info["filename"],
                "file_size": file_info["size"] or len(await file.read()),
                "content_type": file_info["content_type"]
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Video detection failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if file_path:
                self.file_handler.cleanup_file(file_path)
    
    def _validate_image_file(self, file: UploadFile):
        """Validate image file"""
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        max_size = 10 * 1024 * 1024  # 10MB
        if hasattr(file, 'size') and file.size and file.size > max_size:
            raise HTTPException(status_code=400, detail="Image file too large (max 10MB)")
    
    def _validate_audio_file(self, file: UploadFile):
        """Validate audio file"""
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be audio")
        
        max_size = 50 * 1024 * 1024  # 50MB
        if hasattr(file, 'size') and file.size and file.size > max_size:
            raise HTTPException(status_code=400, detail="Audio file too large (max 50MB)")
    
    def _validate_video_file(self, file: UploadFile):
        """Validate video file"""
        if not file.content_type or not file.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="File must be video")
        
        max_size = 100 * 1024 * 1024  # 100MB
        if hasattr(file, 'size') and file.size and file.size > max_size:
            raise HTTPException(status_code=400, detail="Video file too large (max 100MB)")
