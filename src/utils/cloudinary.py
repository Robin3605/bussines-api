import cloudinary
import cloudinary.uploader
from fastapi import HTTPException
from typing import Optional, Dict, Any
from fastapi import HTTPException, UploadFile
from typing import List


async def upload_images_to_cloudinary(files: List[UploadFile], folder: str = "products") -> List[str]:
    urls = []
    try:
        for file in files:
            contents = await file.read()
            result = cloudinary.uploader.upload(
                contents,
                folder=folder,
                resource_type="image"
            )
            if result and "secure_url" in result:
                urls.append(result["secure_url"])
        return urls

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir imágenes: {str(e)}")

def delete_file(file_id: str, resource_type: str = "image") -> Optional[Dict[str, Any]]:
    try:
        # Validar tipos de recurso permitidos
        valid_types = ["image", "javascript", "css", "video", "raw"]
        if resource_type not in valid_types:
            raise ValueError(f"Invalid resource type. Must be one of: {', '.join(valid_types)}")
        
        # Delete the file from Cloudinary
        response = cloudinary.uploader.destroy(file_id, resource_type=resource_type)
        return response
    except Exception as e:
        # logging.error(f"Error deleting file from Cloudinary: {e}")
        raise HTTPException(status_code=500, detail=str(e))









    






    
    
