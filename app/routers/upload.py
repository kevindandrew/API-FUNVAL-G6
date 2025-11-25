from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from app.auth import get_current_admin_user
from app.utils.cloudinary_utils import upload_image

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_admin_user)
):
    """
    Subir imagen a Cloudinary (Solo Admin)
    - Retorna la URL de la imagen para usar en otros endpoints
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="El archivo debe ser una imagen")
        
    result = upload_image(file.file)
    if not result:
        raise HTTPException(500, detail="Error al subir la imagen")
        
    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id")
    }
