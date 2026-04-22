"""
models/cliente.py

Modelo que representa a los clientes del sistema.
Cada cliente puede tener múltiples pedidos y códigos OTP asociados.
"""

from ..extensions import db

class Cliente(db.Model):

    """
    Modelo de cliente en la base de datos.

    Representa a un cliente registrado en el sistema.

    Atributos:
        id_cliente (int): identificador único del cliente.
        cedula (int): número de identificación del cliente.
        nombre (str): nombre del cliente.
        apellido (str): apellido del cliente.
        correo (str): correo electrónico único del cliente.
        movil (str): número de teléfono móvil.

    Relaciones:
        pedidos (list): lista de pedidos asociados al cliente.
        otps (list): lista de códigos OTP generados para el cliente.
    """    

    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    movil = db.Column(db.String(20))

    pedido = db.relationship('Pedido', back_populates='cliente', lazy=True)
    otps = db.relationship('OtpCodigo', back_populates='cliente', lazy=True)
    
