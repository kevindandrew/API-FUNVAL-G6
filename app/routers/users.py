from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.auth import get_current_admin_user, get_current_user, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    """
    Obtener todos los usuarios - Endpoint de prueba para verificar conexión a DB
    """
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener un usuario por ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Crear un nuevo usuario (Solo Admin)
    - Permite crear usuarios con cualquier rol (incluido admin)
    - Hashea la contraseña antes de guardar
    """
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Hashear contraseña
    hashed_password = get_password_hash(user.password)
    
    # Crear nuevo usuario
    db_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password,
        role=user.role
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Actualizar usuario
    - Admin: Puede actualizar CUALQUIER usuario y cambiar CUALQUIER campo (incluido rol).
    - Cliente: Solo puede actualizar SU PROPIO perfil. NO puede cambiar su rol.
    """
    # Verificar permisos
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este usuario"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Filtrar datos enviados (excluir nulos)
    update_data = user_update.dict(exclude_unset=True)
    
    # Regla de seguridad: Si no es admin, eliminar 'role' de los datos a actualizar
    if current_user.role != "admin" and "role" in update_data:
        del update_data["role"]
        
    # Si se actualiza la contraseña, hashearla
    if "password" in update_data:
        update_data["password"] = get_password_hash(update_data["password"])
    
    # Actualizar campos
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user
