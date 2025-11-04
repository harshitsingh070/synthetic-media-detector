import cv2
import tempfile
import os
import subprocess
import numpy as np
from typing import Dict, Any, List
import logging
from .image_detector import ImageDeepfakeDetector
from .audio_detector import AudioDeepfakeDetector

logger = logging.getLogger(__name__)

class VideoDeepfakeDetector:
    def __init__(self):
        self.image_detector = ImageDeepfakeDetector()
        self.audio_detector = AudioDeepfakeDetector()
        self.max_frames = 30
        logger.info("Video detector initialized")
    
    def predict(self, video_path: str) -> Dict[str, Any]:
        """Predict if video is fake or real"""
        try:
            # Extract frames for visual analysis
            frames_results = self._analyze_frames(video_path)
            
            # Extract and analyze audio
            audio_result = self._analyze_audio(video_path)
            
            # Combine results
            visual_score = np.mean([r["fake_probability"] for r in frames_results]) if frames_results else 0.5
            audio_score = audio_result.get("fake_probability", 0.5)
            
            # Weighted fusion (70% visual, 30% audio)
            final_score = 0.7 * visual_score + 0.3 * audio_score
            
            return self._format_result(visual_score, audio_score, final_score, video_path)
            
        except Exception as e:
            logger.error(f"Error during video prediction: {e}")
            return {
                "error": f"Failed to analyze video: {str(e)}",
                "visual_score": 0.5,
                "audio_score": 0.5,
                "final_score": 0.5,
                "prediction": "unknown"
            }
    
    def _analyze_frames(self, video_path: str) -> List[Dict[str, Any]]:
        """Extract and analyze frames from video"""
        try:
            frames = self._extract_frames(video_path)
            results = []
            
            for i, frame in enumerate(frames):
                # Save frame temporarily
                temp_frame = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
                cv2.imwrite(temp_frame.name, frame)
                temp_frame.close()
                
                try:
                    # Analyze frame
                    result = self.image_detector.predict(temp_frame.name)
                    results.append(result)
                finally:
                    # Cleanup temporary frame
                    os.unlink(temp_frame.name)
            
            return results
            
        except Exception as e:
            logger.error(f"Frame analysis failed: {e}")
            return []
    
    def _extract_frames(self, video_path: str) -> List[np.ndarray]:
        """Extract frames from video"""
        try:
            cap = cv2.VideoCapture(video_path)
            frames = []
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if frame_count == 0:
                logger.warning("No frames found in video")
                cap.release()
                return []
            
            # Sample frames evenly
            step = max(1, frame_count // self.max_frames)
            
            for i in range(0, frame_count, step):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret and frame is not None:
                    frames.append(frame)
                
                if len(frames) >= self.max_frames:
                    break
            
            cap.release()
            logger.info(f"Extracted {len(frames)} frames from video")
            return frames
            
        except Exception as e:
            logger.error(f"Frame extraction failed: {e}")
            return []
    
    def _analyze_audio(self, video_path: str) -> Dict[str, Any]:
        """Extract and analyze audio from video"""
        temp_audio = None
        try:
            # Create temporary audio file
            temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_audio.close()
            
            # Extract audio using ffmpeg
            cmd = [
                'ffmpeg', '-i', video_path,
                '-ac', '1',  # mono
                '-ar', '16000',  # 16kHz sample rate
                '-y',  # overwrite output file
                temp_audio.name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.warning(f"FFmpeg failed: {result.stderr}")
                return {"fake_probability": 0.5, "error": "Audio extraction failed"}
            
            # Analyze extracted audio
            return self.audio_detector.predict(temp_audio.name)
            
        except Exception as e:
            logger.error(f"Audio analysis failed: {e}")
            return {"fake_probability": 0.5, "error": str(e)}
        finally:
            # Cleanup temporary audio file
            if temp_audio and os.path.exists(temp_audio.name):
                os.unlink(temp_audio.name)
    
    def _format_result(self, visual_score: float, audio_score: float, 
                      final_score: float, video_path: str) -> Dict[str, Any]:
        """Format video prediction result"""
        prediction = "fake" if final_score > 0.5 else "real"
        confidence = abs(final_score - 0.5) * 2
        
        return {
            "visual_score": float(visual_score),
            "audio_score": float(audio_score),
            "final_score": float(final_score),
            "fake_probability": float(final_score),
            "real_probability": float(1.0 - final_score),
            "prediction": prediction,
            "confidence": float(confidence),
            "model_used": "multimodal_fusion"
        }
