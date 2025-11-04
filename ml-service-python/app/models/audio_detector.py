import torch
import librosa
import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class AudioDeepfakeDetector:
    def __init__(self):
        self.device = self._get_device()
        self.sample_rate = 16000
        self.duration = 4.0  # 4 seconds
        logger.info(f"Audio detector initialized on {self.device}")
    
    def _get_device(self) -> torch.device:
        """Get the best available device"""
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")
    
    def predict(self, audio_path: str) -> Dict[str, Any]:
        """Predict if audio is fake or real"""
        try:
            # Load and preprocess audio
            audio, sr = librosa.load(audio_path, sr=self.sample_rate)
            
            # Ensure fixed duration
            target_length = int(self.sample_rate * self.duration)
            if len(audio) < target_length:
                # Pad if too short
                audio = np.pad(audio, (0, target_length - len(audio)))
            elif len(audio) > target_length:
                # Truncate if too long
                audio = audio[:target_length]
            
            # Extract features (using spectral features as a simple baseline)
            features = self._extract_features(audio)
            
            # Simple heuristic-based detection (replace with actual model)
            fake_prob = self._simple_audio_classifier(features)
            
            return self._format_result(fake_prob, audio_path)
            
        except Exception as e:
            logger.error(f"Error during audio prediction: {e}")
            return {
                "error": f"Failed to analyze audio: {str(e)}",
                "fake_probability": 0.5,
                "real_probability": 0.5,
                "prediction": "unknown"
            }
    
    def _extract_features(self, audio: np.ndarray) -> Dict[str, float]:
        """Extract audio features for classification"""
        try:
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=self.sample_rate)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=self.sample_rate)[0]
            spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=self.sample_rate)[0]
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(audio)[0]
            
            # MFCC features
            mfccs = librosa.feature.mfcc(y=audio, sr=self.sample_rate, n_mfcc=13)
            
            # Chroma features
            chroma = librosa.feature.chroma_stft(y=audio, sr=self.sample_rate)
            
            return {
                "spectral_centroid_mean": np.mean(spectral_centroids),
                "spectral_centroid_std": np.std(spectral_centroids),
                "spectral_rolloff_mean": np.mean(spectral_rolloff),
                "spectral_bandwidth_mean": np.mean(spectral_bandwidth),
                "zcr_mean": np.mean(zcr),
                "mfccs_mean": np.mean(mfccs),
                "mfccs_std": np.std(mfccs),
                "chroma_mean": np.mean(chroma)
            }
        except Exception as e:
            logger.warning(f"Feature extraction failed: {e}")
            return {"error": True}
    
    def _simple_audio_classifier(self, features: Dict[str, float]) -> float:
        """Simple heuristic classifier (replace with actual model)"""
        if "error" in features:
            return np.random.uniform(0.4, 0.6)
        
        # Simple heuristic based on spectral features
        # This is just a placeholder - replace with actual trained model
        score = 0.5
        
        # Add some logic based on features
        if features["spectral_centroid_mean"] > 2000:
            score += 0.1
        if features["zcr_mean"] > 0.1:
            score += 0.1
        if features["mfccs_std"] > 10:
            score += 0.1
        
        # Add some randomness to simulate model uncertainty
        score += np.random.uniform(-0.1, 0.1)
        
        return np.clip(score, 0.0, 1.0)
    
    def _format_result(self, fake_prob: float, audio_path: str) -> Dict[str, Any]:
        """Format prediction result"""
        real_prob = 1.0 - fake_prob
        prediction = "fake" if fake_prob > 0.5 else "real"
        confidence = abs(fake_prob - 0.5) * 2
        
        return {
            "fake_probability": float(fake_prob),
            "real_probability": float(real_prob),
            "prediction": prediction,
            "confidence": float(confidence),
            "model_used": "heuristic_baseline"
        }
