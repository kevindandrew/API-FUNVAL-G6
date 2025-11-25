from app.database import SessionLocal
from app.models.user import User
from app.auth import get_password_hash

def create_admin_user():
    db = SessionLocal()
    try:
        email = "funvaladmin@gmail.com"
        password = "123456789"
        name = "Kevin Rodriguez"
        
        # Verificar si ya existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"El usuario {email} ya existe.")
            # Actualizar a admin si no lo es
            if existing_user.role != "admin":
                existing_user.role = "admin"
                db.commit()
                print("Rol actualizado a admin.")
            return

        hashed_password = get_password_hash(password)
        
        new_user = User(
            email=email,
            password=hashed_password,
            name=name,
            role="admin"
        )
        
        db.add(new_user)
        db.commit()
        print(f"Usuario Admin creado exitosamente: {email}")
        
    except Exception as e:
        print(f"Error creando usuario: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
