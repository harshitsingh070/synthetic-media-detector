#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from huggingface_hub import snapshot_download
import torch
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_pretrained_models():
    """Download all required pretrained models"""
    
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    logger.info("Starting model download process...")
    
    # Model configurations
    models_to_download = [
        {
            "name": "SigLIP Deepfake Detector",
            "repo_id": "prithivMLmods/deepfake-detector-model-v1",
            "local_dir": models_dir / "siglip-deepfake-detector"
        }
    ]
    
    success_count = 0
    
    for model_config in models_to_download:
        try:
            logger.info(f"Downloading {model_config['name']}...")
            
            # Check if model already exists
            if model_config["local_dir"].exists() and any(model_config["local_dir"].iterdir()):
                logger.info(f"Model {model_config['name']} already exists. Skipping...")
                success_count += 1
                continue
            
            # Download model
            snapshot_download(
                repo_id=model_config["repo_id"],
                local_dir=str(model_config["local_dir"]),
                local_dir_use_symlinks=False,
                resume_download=True
            )
            
            logger.info(f"✅ Successfully downloaded {model_config['name']}")
            success_count += 1
            
        except Exception as e:
            logger.error(f"❌ Failed to download {model_config['name']}: {str(e)}")
    
    # Create model info file
    create_model_info_file(models_dir, success_count, len(models_to_download))
    
    logger.info(f"Model download complete! {success_count}/{len(models_to_download)} models downloaded successfully.")
    
    return success_count == len(models_to_download)

def create_model_info_file(models_dir: Path, success_count: int, total_count: int):
    """Create a file with model information"""
    
    info_content = f"""# Pretrained Models Information

## Download Status
- Successfully downloaded: {success_count}/{total_count} models
- Download date: {torch.utils.data.get_worker_info()}

## Available Models

### Image Detection
- **SigLIP Deepfake Detector**
  - Location: siglip-deepfake-detector/
  - Purpose: Binary classification of real vs fake images
  - Architecture: SigLIP-based transformer
  - Performance: ~94% accuracy on standard benchmarks

### Audio Detection  
- **Baseline Audio Classifier**
  - Location: Built-in heuristic model
  - Purpose: Audio deepfake detection using spectral features
  - Architecture: Feature-based classifier
  - Note: This is a baseline implementation

### Video Detection
- **Multi-modal Fusion**
  - Combines image and audio detection results
  - Weighted fusion (70% visual, 30% audio)
  - Supports temporal analysis of video frames

## Usage Notes
- Models are automatically loaded by the ML service
- GPU acceleration is used when available
- Fallback models are used if primary models fail to load
"""
    
    info_file = models_dir / "README.md"
    with open(info_file, "w") as f:
        f.write(info_content)
    
    logger.info(f"Created model info file: {info_file}")

def check_system_requirements():
    """Check if system meets requirements"""
    
    logger.info("Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or python_version.minor < 8:
        logger.error("Python 3.8+ is required")
        return False
    
    logger.info(f"✅ Python version: {python_version.major}.{python_version.minor}")
    
    # Check PyTorch
    try:
        import torch
        logger.info(f"✅ PyTorch version: {torch.__version__}")
        
        # Check CUDA availability
        if torch.cuda.is_available():
            logger.info(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            logger.info("ℹ️ CUDA not available, using CPU")
            
    except ImportError:
        logger.warning("⚠️ PyTorch not found, will be installed with requirements")
    
    # Check available disk space
    import shutil
    total, used, free = shutil.disk_usage(".")
    free_gb = free // (1024**3)
    
    if free_gb < 5:
        logger.warning(f"⚠️ Low disk space: {free_gb}GB free (recommended: 5GB+)")
    else:
        logger.info(f"✅ Disk space: {free_gb}GB free")
    
    return True

def main():
    """Main function"""
    
    logger.info("🤖 Pretrained Model Download Script")
    logger.info("=" * 50)
    
    # Check system requirements
    if not check_system_requirements():
        logger.error("System requirements not met")
        sys.exit(1)
    
    # Download models
    try:
        success = download_pretrained_models()
        if success:
            logger.info("🎉 All models downloaded successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Some models failed to download")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Download process failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
