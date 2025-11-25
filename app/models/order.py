from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default='pendiente', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación con order_details
    details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
