"""
models/__init__.py

Este módulo centraliza la importación de todos los modelos de la
aplicación. Esto permite que SQLAlchemy registre correctamente
todas las tablas cuando se inicializa la aplicación.

Los modelos se agrupan según su funcionalidad:
- usuarios
- pedidos
- autenticación (OTP)
"""
# Modelos relacionados con usuarios
from .users import Cliente

# Modelos relacionados con pedidos
from .orders import Pedido, Producto, DetallePedido, Estado, HistorialEstadoPedido, Notificacion

# Modelos relacionados con autenticación por código OTP
from .otp_code import OtpCodigo
