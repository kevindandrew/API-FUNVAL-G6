import cloudinary
import cloudinary.uploader
from app.config import settings

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

def upload_image(file_file, folder: str = "funval_g6_products"):
    """
    Sube una imagen a Cloudinary
    
    Args:
        file_file: El archivo de imagen recibido del endpoint
        folder: Carpeta en Cloudinary donde guardar la imagen
        
    Returns:
        dict: Respuesta de Cloudinary con url, public_id, etc.
    """
    try:
        # Subir imagen
        result = cloudinary.uploader.upload(file_file, folder=folder)
        return result
    except Exception as e:
        print(f"Error subiendo imagen a Cloudinary: {e}")
        return None
