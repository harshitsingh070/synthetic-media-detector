import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional
from fastapi import UploadFile, HTTPException

class FileHandler:
    def __init__(self, temp_dir: str = "./temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
    
    async def save_upload_file(self, upload_file: UploadFile, suffix: str = None) -> str:
        """Save uploaded file to temporary directory"""
        try:
            # Create temporary file
            if suffix:
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, 
                    suffix=suffix, 
                    dir=self.temp_dir
                )
            else:
                temp_file = tempfile.NamedTemporaryFile(
                    delete=False, 
                    dir=self.temp_dir
                )
            
            # Write file content
            content = await upload_file.read()
            temp_file.write(content)
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    def cleanup_file(self, file_path: str) -> None:
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Warning: Failed to cleanup file {file_path}: {e}")
    
    def get_file_info(self, upload_file: UploadFile) -> dict:
        """Get file information"""
        return {
            "filename": upload_file.filename,
            "content_type": upload_file.content_type,
            "size": upload_file.size if hasattr(upload_file, 'size') else None
        }
