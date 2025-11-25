# ============================================

# 📦 MÓDULO 2: PRODUCTOS - GUÍA DE PRUEBAS (ACTUALIZADA)

# ============================================

## 📋 Requisitos previos

- Servidor corriendo: `uvicorn app.main:app --reload`
- Usuario ADMIN creado y Token obtenido

## 🌐 URL Base

http://localhost:8000

---

## 🔐 Paso 1: Subir Imagen (Nuevo Endpoint)

**POST** `/upload/`
**Auth:** Requiere Token Admin

Este es el único endpoint que usa `multipart/form-data`.
Sube tu imagen aquí primero.

### Response Esperado:

```json
{
  "url": "https://res.cloudinary.com/...",
  "public_id": "funval_g6_products/..."
}
```

**⚠️ COPIA LA URL QUE TE DEVUELVE**

---

## 📌 Paso 2: Crear Producto (JSON Puro)

**POST** `/products/`
**Auth:** Requiere Token Admin

Ahora puedes usar el editor JSON de Swagger o Postman.
Pega la URL de la imagen en el campo `image_url`.

### Body (JSON):

```json
{
  "name": "Laptop Gamer",
  "description": "Laptop super potente",
  "price": 1500.0,
  "stock": 10,
  "category": "Tecnología",
  "image_url": "https://res.cloudinary.com/..."
}
```

### Response Esperado (201 Created):

```json
{
  "name": "Laptop Gamer",
  "description": "Laptop super potente",
  "price": 1500.0,
  "stock": 10,
  "category": "Tecnología",
  "image_url": "https://res.cloudinary.com/...",
  "id": 1,
  "created_at": "..."
}
```

---

## 📌 Otros Endpoints (Sin Cambios)

- **GET** `/products/` (Listar)
- **GET** `/products/{id}` (Detalle)
- **PUT** `/products/{id}` (Actualizar - JSON)
- **DELETE** `/products/{id}` (Eliminar)
