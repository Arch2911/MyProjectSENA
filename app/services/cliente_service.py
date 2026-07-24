from ..extensions import db
from ..models.users import Cliente
from ..models.orders import Pedido

from app.services import otp_service
from app.services import sms_service

from ..services.constants import CODIGO_VALIDO, CLIENTE_NO_EXISTE, OTP_ENVIADO

# Función para buscar al cliente por cédula
def buscar_cliente(cedula):

    cliente = Cliente.query.filter_by(cedula=cedula).first() # se filtra por cedula al cliente.

    if cliente is None:     
        return CLIENTE_NO_EXISTE

    otp_service.crear_otp(cliente.id_cliente, cliente.movil)


    return OTP_ENVIADO


def verificacion_cliente_otp(cedula, codigo):

    cliente = Cliente.query.filter_by(cedula=cedula).first()

    if cliente is None:
        return CLIENTE_NO_EXISTE
    
    id_cliente = cliente.id_cliente

    estado_codigo = otp_service.verificar_otp(id_cliente, codigo)

    if estado_codigo != CODIGO_VALIDO:
        return estado_codigo
    
    return CODIGO_VALIDO

