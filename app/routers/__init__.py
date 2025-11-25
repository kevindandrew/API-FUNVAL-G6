from .users import router as users_router
from .auth import router as auth_router
from .products import router as products_router
from .upload import router as upload_router
from .orders import router as orders_router

__all__ = ["users_router", "auth_router", "products_router", "upload_router", "orders_router"]
