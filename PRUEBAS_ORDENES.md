# ============================================

# 🛒 MÓDULO 3: ÓRDENES - GUÍA DE PRUEBAS

# ============================================

## 📋 Requisitos previos

- Servidor corriendo: `uvicorn app.main:app --reload`
- Usuario Cliente (para comprar) y Usuario Admin (para gestionar)
- Productos creados con stock disponible

## 🌐 URL Base

http://localhost:8000

---

## 📌 ENDPOINT 1: Crear Orden (Comprar)

**POST** `/orders/`
**Auth:** Requiere Token (Cualquier usuario logueado)

### Body (JSON):

```json
{
  "items": [
    { "product_id": 1, "quantity": 2 },
    { "product_id": 2, "quantity": 1 }
  ]
}
```

### Response Esperado (201 Created):

```json
{
  "id": 10,
  "user_id": 5,
  "total": 150.5,
  "status": "pendiente",
  "created_at": "...",
  "user_name": null
}
```

### Pruebas Críticas:

- ✅ **Stock Suficiente:** La orden se crea y el stock del producto disminuye.
- ❌ **Stock Insuficiente:** Intenta pedir más de lo que hay. Debe dar error 400 y NO crear la orden.
- ❌ **Producto Inexistente:** Debe dar error 404.

---

## 📌 ENDPOINT 2: Ver Historial de Órdenes

**GET** `/orders/`
**Auth:** Requiere Token

- **Si eres Cliente:** Solo ves TUS órdenes.
- **Si eres Admin:** Ves TODAS las órdenes (ordenadas por fecha).

---

## 📌 ENDPOINT 3: Ver Detalle de Orden

**GET** `/orders/{id}`
**Auth:** Requiere Token

Muestra el detalle completo con los productos comprados.

### Response Esperado:

```json
{
  "id": 10,
  "status": "pendiente",
  "items": [
    {
      "product_id": 1,
      "product_name": "Laptop Gamer",
      "quantity": 2,
      "price": 1500.0,
      "subtotal": 3000.0
    }
  ]
}
```

---

## 📌 ENDPOINT 4: Cambiar Estado (Cobrar/Entregar)

**PATCH** `/orders/{id}/status`
**Auth:** Requiere Token ADMIN

### Body (JSON):

```json
{
  "status": "pagado"
}
```

Valores permitidos: `pendiente`, `pagado`, `entregado`.
