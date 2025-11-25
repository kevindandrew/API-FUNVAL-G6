from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    """Schema para registro de usuario"""
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    """Schema para login"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema para respuesta de token"""
    access_token: str
    token_type: str
    user_role: str
    user_name: str

class UserProfile(BaseModel):
    """Schema para perfil de usuario"""
    id: int
    email: str
    name: str
    role: str
    
    class Config:
        from_attributes = True
