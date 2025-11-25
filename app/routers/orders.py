from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.product import Product
from app.models.user import User
from app.schemas.orders import OrderCreate, OrderResponse, OrderDetailResponse, OrderStatusUpdate, OrderItemResponse
from app.auth import get_current_user, get_current_admin_user

router = APIRouter(
    prefix="/orders",
    tags=["Órdenes"]
)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    🔥 Crear Orden (Comprar)
    - Valida stock disponible
    - Calcula total server-side
    - Resta stock
    - Crea registros de orden y detalles
    """
    if not order_data.items:
        raise HTTPException(status_code=400, detail="La orden no puede estar vacía")

    # 1. Validar stock y calcular total
    total_amount = 0
    items_to_process = [] # Lista de tuplas (producto_db, cantidad, precio_congelado)

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto con ID {item.product_id} no encontrado")
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400, 
                detail=f"Stock insuficiente para '{product.name}'. Disponible: {product.stock}, Solicitado: {item.quantity}"
            )
        
        # Calcular subtotal y acumular total
        item_price = product.price # Precio congelado al momento de la compra
        subtotal = item_price * item.quantity
        total_amount += subtotal
        
        items_to_process.append({
            "product": product,
            "quantity": item.quantity,
            "price": item_price
        })

    # 2. Crear la Orden (Cabecera)
    new_order = Order(
        user_id=current_user.id,
        total=total_amount,
        status="pendiente"
    )
    db.add(new_order)
    db.flush() # Para obtener el ID de la orden antes del commit final

    # 3. Crear Detalles y Actualizar Stock
    for item_data in items_to_process:
        product = item_data["product"]
        quantity = item_data["quantity"]
        price = item_data["price"]
        
        # Crear detalle
        order_detail = OrderDetail(
            order_id=new_order.id,
            product_id=product.id,
            quantity=quantity,
            price=price
        )
        db.add(order_detail)
        
        # Restar stock
        product.stock -= quantity
    
    # 4. Confirmar Transacción
    db.commit()
    db.refresh(new_order)
    
    return new_order

@router.get("/", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Ver Historial de Órdenes
    - Cliente: Ve solo SUS órdenes
    - Admin: Ve TODAS las órdenes
    """
    if current_user.role == "admin":
        orders = db.query(Order).order_by(Order.created_at.desc()).all()
        # Enriquecer con nombre de usuario para el admin
        for order in orders:
            user = db.query(User).filter(User.id == order.user_id).first()
            order.user_name = user.name if user else "Desconocido"
        return orders
    else:
        return db.query(Order).filter(Order.user_id == current_user.id).order_by(Order.created_at.desc()).all()

@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Ver Detalle de una Orden
    - Cliente: Solo puede ver sus propias órdenes
    - Admin: Puede ver cualquier orden
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Verificar permisos
    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta orden")
    
    # Construir respuesta con detalles enriquecidos (nombre del producto)
    response_items = []
    for detail in order.details:
        product = db.query(Product).filter(Product.id == detail.product_id).first()
        response_items.append(OrderItemResponse(
            product_id=detail.product_id,
            product_name=product.name if product else "Producto Eliminado",
            quantity=detail.quantity,
            price=detail.price,
            subtotal=detail.price * detail.quantity
        ))
    
    # Mapear manualmente para incluir items procesados
    response = OrderDetailResponse(
        id=order.id,
        user_id=order.user_id,
        total=order.total,
        status=order.status,
        created_at=order.created_at,
        items=response_items
    )
    
    return response

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """
    Cambiar Estado de Orden (Solo Admin)
    - Valores permitidos: pendiente, pagado, entregado
    """
    valid_statuses = ["pendiente", "pagado", "entregado"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Permitidos: {valid_statuses}")
        
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
        
    order.status = status_update.status
    db.commit()
    db.refresh(order)
    
    return order
