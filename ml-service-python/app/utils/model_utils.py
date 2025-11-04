import torch
import os
from pathlib import Path
from huggingface_hub import snapshot_download
from typing import Optional

class ModelManager:
    def __init__(self, cache_dir: str = "./models"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def download_huggingface_model(self, model_name: str, local_dir: Optional[str] = None) -> str:
        """Download model from HuggingFace Hub"""
        if local_dir is None:
            local_dir = self.cache_dir / model_name.replace("/", "_")
        
        try:
            if not os.path.exists(local_dir):
                print(f"Downloading model {model_name}...")
                snapshot_download(
                    repo_id=model_name,
                    local_dir=local_dir,
                    local_dir_use_symlinks=False
                )
            
            return str(local_dir)
            
        except Exception as e:
            raise Exception(f"Failed to download model {model_name}: {str(e)}")
    
    def check_gpu_availability(self) -> bool:
        """Check if GPU is available"""
        return torch.cuda.is_available()
    
    def get_device(self) -> torch.device:
        """Get optimal device for inference"""
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")
