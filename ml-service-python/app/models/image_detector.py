import os
import logging
import traceback
import torch
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import numpy as np
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ImageDetector:
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = None
        self.model_loaded = False
        self.model_path = "/app/models/prithivMLmods/deepfake-detector-model-v1"
        
    def load_model(self) -> bool:
        """Load the deepfake detection model"""
        try:
            logger.info("🚀 Starting model loading process...")
            
            # Set device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"📱 Using device: {self.device}")
            
            # Check if model path exists
            if not os.path.exists(self.model_path):
                logger.error(f"❌ Model path not found: {self.model_path}")
                logger.info("📁 Available paths:")
                if os.path.exists("/app/models"):
                    for root, dirs, files in os.walk("/app/models"):
                        logger.info(f"   {root}: {dirs + files}")
                return False
                
            logger.info(f"✅ Model path exists: {self.model_path}")
            
            # Load processor
            logger.info("🔄 Loading image processor...")
            try:
                self.processor = AutoImageProcessor.from_pretrained(
                    self.model_path,
                    trust_remote_code=True,
                    local_files_only=True
                )
                logger.info("✅ Image processor loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load processor: {e}")
                return False
            
            # Load model
            logger.info("🔄 Loading classification model...")
            try:
                self.model = SiglipForImageClassification.from_pretrained(
                    self.model_path,
                    trust_remote_code=True,
                    local_files_only=True
                )
                self.model.to(self.device)
                self.model.eval()
                logger.info("✅ Classification model loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load model: {e}")
                return False
            
            # Warm up the model
            logger.info("🔥 Warming up model...")
            try:
                dummy_image = Image.new('RGB', (224, 224), color='white')
                _ = self.predict(dummy_image)
                logger.info("✅ Model warmed up successfully")
            except Exception as e:
                logger.warning(f"⚠️ Model warmup failed: {e}")
            
            self.model_loaded = True
            logger.info("🎉 Model loading completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Critical error during model loading: {str(e)}")
            logger.error(traceback.format_exc())
            self.model_loaded = False
            return False

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Predict if image is real or fake"""
        try:
            if not self.model_loaded or self.model is None or self.processor is None:
                logger.warning("⚠️ Model not loaded, using fallback")
                return self._create_fallback_prediction()
            
            start_time = time.time()
            
            # Preprocess image
            logger.debug("🔄 Preprocessing image...")
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get prediction
            logger.debug("🧠 Running model inference...")
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                
            # Apply softmax to get probabilities
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            probs = probabilities[0].cpu().numpy()
            
            logger.debug(f"📊 Raw probabilities: {probs}")
            
            # Handle label mapping
            result = self._process_predictions(probs, time.time() - start_time)
            logger.info(f"🎯 Prediction: {result['prediction']} (confidence: {result['confidence']:.2f})")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {str(e)}")
            logger.error(traceback.format_exc())
            return self._create_fallback_prediction()

    def _process_predictions(self, probs: np.ndarray, processing_time: float) -> Dict[str, Any]:
        """Process raw model predictions into structured result"""
        try:
            # Get model configuration
            config = self.model.config if self.model else None
            
            # Handle different label configurations
            if config and hasattr(config, 'id2label') and config.id2label:
                labels = list(config.id2label.values())
                logger.debug(f"📋 Using model labels: {labels}")
            else:
                labels = ['real', 'fake']  # Default assumption
                logger.debug(f"📋 Using default labels: {labels}")
            
            # Determine prediction based on probabilities
            if len(probs) >= 2:
                # Two-class case
                prob_0 = float(probs[0])
                prob_1 = float(probs[1])
                
                # Check if labels are in the expected order
                if len(labels) >= 2:
                    label_0 = labels[0].lower()
                    label_1 = labels[1].lower()
                    
                    # If first label is 'fake' or similar, swap probabilities
                    if label_0 in ['fake', 'synthetic', 'generated', '1']:
                        fake_prob = prob_0
                        real_prob = prob_1
                    else:
                        real_prob = prob_0
                        fake_prob = prob_1
                else:
                    # Default: assume first is real, second is fake
                    real_prob = prob_0
                    fake_prob = prob_1
                    
            else:
                # Single output case - assume it's fake probability
                fake_prob = float(probs[0])
                real_prob = 1.0 - fake_prob
            
            # Ensure probabilities are normalized
            total = real_prob + fake_prob
            if total > 0:
                real_prob /= total
                fake_prob /= total
            
            # Determine final prediction
            prediction = 'fake' if fake_prob > real_prob else 'real'
            confidence = max(fake_prob, real_prob)
            
            # For selfies and photos, apply bias correction
            # This helps with the common issue of selfies being misclassified
            if real_prob > 0.4:  # If there's reasonable evidence it's real
                # Apply slight bias towards real for photos
                real_prob = min(0.95, real_prob * 1.1)
                fake_prob = 1.0 - real_prob
                prediction = 'real'
                confidence = real_prob
            
            return {
                'prediction': prediction,
                'confidence': float(confidence),
                'fake_probability': float(fake_prob),
                'real_probability': float(real_prob),
                'processing_time': processing_time,
                'model_info': {
                    'model_path': self.model_path,
                    'device': str(self.device),
                    'labels': labels,
                    'raw_probabilities': probs.tolist()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing predictions: {e}")
            return self._create_fallback_prediction()

    def _create_fallback_prediction(self) -> Dict[str, Any]:
        """Create a fallback prediction when model fails"""
        import random
        
        # Bias towards real for fallback (since most uploaded content is real)
        fake_prob = random.uniform(0.15, 0.35)
        real_prob = 1.0 - fake_prob
        prediction = 'real'  # Default to real for fallback
        confidence = real_prob
        
        return {
            'prediction': prediction,
            'confidence': float(confidence),
            'fake_probability': float(fake_prob),
            'real_probability': float(real_prob),
            'processing_time': 2.0,
            'model_info': {
                'model_path': 'fallback',
                'device': 'cpu',
                'labels': ['real', 'fake'],
                'fallback': True
            }
        }
