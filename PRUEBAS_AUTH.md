# ============================================

# 🔐 MÓDULO 1: AUTENTICACIÓN - GUÍA DE PRUEBAS

# ============================================

## 📋 Requisitos previos

- Servidor corriendo: uvicorn app.main:app --reload
- Base de datos PostgreSQL activa
- Navegador web o Postman/Thunder Client

## 🌐 URL Base

http://localhost:8000

## 📌 ENDPOINT 1: Registrar Nuevo Usuario

POST http://localhost:8000/auth/register

### Request Body (JSON):

```json
{
  "email": "juan@mail.com",
  "password": "password123",
  "name": "Juan Perez"
}
```

### Response Esperado (201 Created):

```json
{
  "id": 1,
  "email": "juan@mail.com",
  "name": "Juan Perez",
  "role": "cliente"
}
```

### Pruebas adicionales:

- ✅ Registrar otro usuario: maria@mail.com
- ❌ Intentar registrar el mismo email (debe dar error 400)

---

## 📌 ENDPOINT 2: Iniciar Sesión

POST http://localhost:8000/auth/login

### Request Body (JSON):

```json
{
  "email": "juan@mail.com",
  "password": "password123"
}
```

### Response Esperado (200 OK):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_role": "cliente",
  "user_name": "Juan Perez"
}
```

### Pruebas adicionales:

- ❌ Intentar login con contraseña incorrecta (debe dar error 401)
- ❌ Intentar login con email inexistente (debe dar error 401)

**⚠️ IMPORTANTE: Copia el `access_token` del response, lo necesitarás para el siguiente endpoint**

---

## 📌 ENDPOINT 3: ¿Quién soy yo? (Perfil)

GET http://localhost:8000/auth/me

### Headers:

```
Authorization: Bearer <TU_ACCESS_TOKEN_AQUÍ>
```

### Response Esperado (200 OK):

```json
{
  "id": 1,
  "email": "juan@mail.com",
  "name": "Juan Perez",
  "role": "cliente"
}
```

### Pruebas adicionales:

- ❌ Intentar sin token (debe dar error 401)
- ❌ Intentar con token inválido (debe dar error 401)

---

## 🔍 Verificar en Base de Datos

Puedes verificar los usuarios creados en PostgreSQL con:

```sql
SELECT id, email, name, role, created_at FROM users;
```

La contraseña debe verse hasheada (no en texto plano).

---

## 🎯 CURL Examples (Para copiar y pegar en terminal)

### 1. Registro:

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"juan@mail.com\",\"password\":\"password123\",\"name\":\"Juan Perez\"}"
```

### 2. Login:

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"juan@mail.com\",\"password\":\"password123\"}"
```

### 3. Perfil (reemplaza TOKEN con tu token real):

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer TOKEN"
```

---

## 📚 Documentación Interactiva

FastAPI genera documentación automática:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

¡Usa Swagger UI para probar los endpoints de forma visual! 🎉
