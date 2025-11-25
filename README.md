# 🛒 Backend E-commerce FunVal G6

¡Bienvenido al backend del proyecto final! Este es un sistema robusto de E-commerce construido con **FastAPI** y **PostgreSQL**.

## 🚀 Tecnologías

- **Python 3.10+**
- **FastAPI**: Framework moderno y rápido para APIs.
- **PostgreSQL**: Base de datos relacional.
- **SQLAlchemy**: ORM para interactuar con la BD.
- **Pydantic**: Validación de datos.
- **JWT + Bcrypt**: Seguridad y autenticación.
- **Cloudinary**: Almacenamiento de imágenes en la nube.

---

## 🛠️ Configuración e Instalación

### 1. Clonar y Entorno Virtual

```bash
# Clonar repositorio
git clone <url-del-repo>
cd backend-funval-g6

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`) y configura tus credenciales:

```ini
DATABASE_URL=postgresql://postgres:password@localhost/funvalG6
SECRET_KEY=tu_clave_secreta_super_segura
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
```

### 4. Crear Usuario Administrador

Hemos incluido un script para crear un superusuario rápidamente:

```bash
python create_admin.py
```

Esto creará al usuario `funvaladmin@gmail.com` con contraseña `123456789`.

### 5. Iniciar Servidor

```bash
uvicorn app.main:app --reload
```

El servidor correrá en: `http://localhost:8000`

---

## 📚 Documentación de la API (Swagger UI)

Visita **`http://localhost:8000/docs`** para ver la documentación interactiva y probar los endpoints.

---

## 🧪 Guía de Uso y Endpoints Principales

### 🔐 Módulo 1: Autenticación (`/auth`)

Para acceder a las funciones protegidas, necesitas un Token.

1.  **Registrarse**: `POST /auth/register`
2.  **Iniciar Sesión**: `POST /auth/login`
    - Te devolverá un `access_token`.
    - Copia este token.
    - En Swagger, haz clic en el botón **Authorize 🔓** (arriba a la derecha) y pégalo.

### 📦 Módulo 2: Productos (`/products`)

_Solo los administradores pueden crear, editar o borrar productos._

**Pasos para crear un producto:**

1.  **Subir Imagen**: `POST /upload`
    - Sube el archivo de imagen.
    - Copia la `url` que te devuelve.
2.  **Crear Producto**: `POST /products`
    - Envía el JSON con los datos y pega la URL de la imagen en `image_url`.

### 🛒 Módulo 3: Órdenes (`/orders`)

El corazón del negocio.

1.  **Comprar**: `POST /orders`
    - Envía una lista de productos y cantidades.
    - El sistema valida el stock y calcula el total automáticamente.
2.  **Mis Órdenes**: `GET /orders`
    - Los clientes ven su historial de compras.
    - Los administradores ven todas las ventas.
3.  **Cambiar Estado**: `PATCH /orders/{id}/status`
    - Solo Admin. Cambia de `pendiente` -> `pagado` -> `entregado`.

---

## 📂 Estructura del Proyecto

```
app/
├── models/      # Tablas de la Base de Datos (SQLAlchemy)
├── schemas/     # Validación de Datos (Pydantic)
├── routers/     # Endpoints de la API (Rutas)
├── utils/       # Funciones auxiliares (Cloudinary, etc.)
├── auth.py      # Lógica de seguridad (JWT, Hash)
├── config.py    # Configuración de entorno
├── database.py  # Conexión a PostgreSQL
└── main.py      # Punto de entrada de la aplicación
```

---

¡Éxito en tu proyecto! 🎓
