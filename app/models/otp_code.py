"""
models/otp_code.py

Modelo relacionado con la gestión de códigos OTP en el sistema.
"""

from ..extensions import db
from sqlalchemy.sql import func

class OtpCodigo(db.Model):

    """
    Modelo del código OTP en base de datos.
    
    Representa los códigos OTP solicitados por el cliente para verificar la identidad del cliente y acceder al pedido en el sistema.

    Atributos:
        id_otp (int): identificador único del otp.
        codigo (string): código numérico de 6 dígitos.
        fecha_creacion (datetime): fecha de la creación del código.
        usado (bool): indica si el código fue usado.
        expiracion (datetime): tiempo en que expira el código.

    Foráneas:
        id_cliente (int): identificador de cliente asociado a OtpCodigo.
    """

    __tablename__ = 'otp'

    id_otp = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    fecha_creacion = db.Column(db.DateTime(timezone=True), server_default=func.now())
    usado = db.Column(db.Boolean, default=False, nullable=False)
    expiracion = db.Column(db.DateTime(timezone=True), nullable=False)

    cliente = db.relationship('Cliente', back_populates='otps', lazy=True)
