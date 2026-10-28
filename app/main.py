from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import engine, Base
from app.routers import users_router, auth_router, products_router, upload_router, orders_router

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# create_all no agrega columnas a tablas que ya existen:
# agregamos avatar_url a 'users' si la tabla se creó antes de esta columna
with engine.begin() as conn:
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url TEXT"))

app = FastAPI(
    title="FunVal G6 E-Commerce API",
    description="API para sistema de e-commerce con PostgreSQL",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)
app.include_router(upload_router)
app.include_router(orders_router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a FunVal G6 E-Commerce API",
        "status": "online",
        "database": "PostgreSQL conectado ✅"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
