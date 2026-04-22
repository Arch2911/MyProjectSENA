"""
models/orders.py

Modelos relacionados con la gestión de pedidos del sistema.
Incluye pedidos, producto, detalles del pedido, estados, historial
de estados y notificaciones.

"""

from ..extensions import db
from sqlalchemy.sql import func # permite que al ingresar un registro directamente desde la BD(MySQL) también registre la fecha

class Pedido(db.Model):

    """
    Modelo de pedido en la base de datos.

    Representa los pedidos realizados por los clientes en el sistema.

    Atributos:
        id_pedido (int): identificador único del pedido.
        numero_pedido (string): número con que se registro o se genero el pedido
        fecha_pedido (datetime): fecha en que fue realizado el pedido
        total (int): valor de la compra realizada en el pedido
    
    Foraneas:
        id_cliente (int): identificador del cliente asociado al pedido
        estado_actual_id (int): identificador del estado actual del pedido

    Relaciones:
        detalles (list): lista de detalles de pedido asociados al pedido
        historial_estados (list): lista historial de estado de pedido asociado al pedido
        notificaciones (list): lista de notifiaciones asociadas al pedido
    """

    __tablename__ = 'pedidos'

    id_pedido = db.Column(db.Integer, primary_key=True)
    numero_pedido = db.Column(db.String(100), unique=True)
    fecha_pedido = db.Column(db.DateTime(timezone=True), server_default=func.now())
    total = db.Column(db.Integer, nullable=False)
    
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    estado_actual_id = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)

    cliente = db.relationship('Cliente', back_populates='pedido', lazy=True)
    detalles = db.relationship('DetallePedido', back_populates='pedido', lazy=True)
    historial_estados = db.relationship('HistorialEstadoPedido', back_populates='pedido', lazy=True)
    notificaciones = db.relationship('Notificacion', back_populates='pedido', lazy=True)
    estado = db.relationship('Estado', back_populates='pedido', lazy=True)

class Producto(db.Model):

    """
    Modelo de producto en la base de datos.

    Representa a los productos registrados en el sistema.

    Atributos:
        id_producto (int): identificador único del producto.
        nombre (string): nombre del producto.
        descripcion (text): descrición del producto.
        precio (int): precio del producto.

    Relaciones:
        detalles (list): lista de detalles de pedido asociada al producto.
    """

    __tablename__ = 'productos'

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Integer, nullable=False)

    detalles = db.relationship('DetallePedido', back_populates='producto', lazy=True)

class DetallePedido(db.Model):

    """
    Modelo de detalle del pedido en la base de datos.

    Representa los detalles de cada pedido registrados en el sistema.

    Atributos:
        id_detalle (int): identificado único del detalle del pedido.
        cantidad (int): cantidad del producto en el pedido.
        precio_unitario (int): precio del producto por unidad.
        subtotal (int): total calculado para este producto en el pedido.

    Foráneas:
        id_pedido (int): identificador del pedido asociado al detalle.
        id_producto (int): identificador del producto asociado al detalle.
    """

    __tablename__ = 'detalle_pedido'

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)

    pedido = db.relationship('Pedido', back_populates='detalles', lazy=True)
    producto = db.relationship('Producto', back_populates='detalles', lazy=True)

class Estado(db.Model):

    """
    Modelo estado en la base de datos

    Representa los posibles estados de un pedido en el sistema.

    Atributos:
        id_estado (int): identificador único del estado.
        nombre_estado (string): nombre del estado.
    
    Relaciones:
        pedidos (list): lista de pedidos asociadas estado
        historialestados (list): lista de historial de estados del pedido asiciada a estado
    """

    __tablename__ = 'estados'

    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(120), nullable=False)

    pedido = db.relationship('Pedido', back_populates='estado', lazy=True)
    historial_estados = db.relationship('HistorialEstadoPedido', back_populates='estado', lazy=True)

class HistorialEstadoPedido(db.Model):

    """
    Modelo historialEstadoPedido en la base de datos.

    Representa el historial de los estados que ha tenido pedido en el sistema.
    Se puede hacer un seguimiento de todo los estados por los que ha pasado 
    un pedido a lo largo del tiempo.

    Atributos:
        id_historial (int): identificador único del historial.
        fecha_actualizacion (datetime): fecha en que se actulizo el estado de un pedido.

    Foráneas:
        id_pedido (int): identificador de pedido asociado al historial.
        id_estado (int): identificador de estado asociado al historial.
    """

    __tablename__ = 'historial_estados'

    id_historial = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_estado = db.Column(db.Integer, db.ForeignKey('estados.id_estado'), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    pedido = db.relationship('Pedido', back_populates='historial_estados', lazy=True)
    estado = db.relationship('Estado', back_populates='historial_estados', lazy=True)


class Notificacion(db.Model):

    """
    Modelo de notificaciones en base de datos.

    Representa las notificaciones que se realizan del cambio de estados de un pedido
    para que asi el cliente lleve un seguimiento de su pedido.

    Atributos:
        id_notificacion (int): identificador único de la notificación.
        medio (string): medio por el cual se enviara la notificación.
        mensaje (text): información o detalle que acompañara la notificación.
        fecha_envio (datetime): fecha en que se envia la notificación.
        estado_envio (string): estado actual que se notifica del pedido.
    """

    __tablename__ = 'notificaciones'

    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    medio = db.Column(db.String(120), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime(timezone=True), nullable=True)
    estado_envio = db.Column(db.String(120), nullable=False)

    pedido = db.relationship('Pedido', back_populates='notificaciones', lazy=True)