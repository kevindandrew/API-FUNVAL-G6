from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, Token, UserProfile
from app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.utils.cloudinary_utils import upload_image

MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5MB

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/register", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    📝 Registrar Nuevo Usuario
    
    - Público: Cualquiera se puede registrar
    - El rol por defecto es 'cliente'
    - La contraseña se hashea automáticamente con bcrypt
    """
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear nuevo usuario con contraseña hasheada
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        password=hashed_password,
        name=user_data.name,
        role="cliente"  # Por defecto siempre es cliente
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    🔐 Iniciar Sesión (Login)
    
    - Público: Cualquiera puede intentar loguearse
    - Devuelve un token JWT válido por 30 minutos
    - Incluye información del rol y nombre para el frontend
    """
    # Buscar usuario por email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # Verificar que el usuario existe y la contraseña es correcta
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_role": user.role,
        "user_name": user.name
    }

@router.get("/me", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    """
    👤 ¿Quién soy yo? (Helper Frontend) ⭐
    
    - Requiere Token (Usuario debe estar logueado)
    - Utilidad: Verificar si el token sigue válido
    - Útil para recargar datos del usuario al refrescar la página
    """
    return current_user

@router.put("/perfil", response_model=UserProfile)
def update_profile(
    name: Optional[str] = Form(None),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    🖼️ Actualizar Mi Perfil (con foto)
    
    - Requiere Token (Usuario debe estar logueado)
    - Se envía como multipart/form-data (FormData en el frontend)
    - Campos opcionales: 'name' (texto) y 'foto' (imagen, máx 5MB)
    - La foto se sube a Cloudinary y se guarda su URL en 'avatar_url'
    """
    if name is not None:
        name = name.strip()
        if len(name) < 3:
            raise HTTPException(400, detail="El nombre debe tener al menos 3 caracteres")
        current_user.name = name
    
    if foto is not None and foto.filename:
        if not foto.content_type or not foto.content_type.startswith("image/"):
            raise HTTPException(400, detail="El archivo debe ser una imagen")
        
        contents = foto.file.read()
        if len(contents) > MAX_AVATAR_SIZE:
            raise HTTPException(400, detail="La imagen no puede superar los 5MB")
        
        result = upload_image(contents, folder="funval_g6_avatars")
        if not result:
            raise HTTPException(500, detail="Error al subir la imagen")
        current_user.avatar_url = result.get("secure_url")
    
    db.commit()
    db.refresh(current_user)
    return current_user
