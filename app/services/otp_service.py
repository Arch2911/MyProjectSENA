
from ..extensions import db
from ..models.otp_code import OtpCodigo
from datetime import datetime, UTC, timedelta
import secrets
from app.services.sms_service import envio_sms

from ..services.constants import CODIGO_EXPIRADO, CODIGO_INVALIDO, CODIGO_NO_EXISTE, CODIGO_VALIDO, OTP_MINUTOS_EXPIRACION

def generar_codigo():

    """
    Genera un código OTP aleatorio de 6 dígitos.

    Lógica:
    - Se utiliza el módulo secrets para generar un número seguro.
    - El número generado se formatea para garantizar que siempre tenga 6 dígitos.

    Returns:
        str: Código OTP de 6 dígitos.
    """

    otp = f'{secrets.randbelow(1000000):06}'

    return otp

def crear_otp(id_cliente, movil):

    """
    Crea un nuevo código OTP para un cliente.

    Reglas de negocio:
    1. Un cliente solo puede tener un OTP activo.
    2. Si existen OTP activos, se marcan como usados.
    3. Se genera un nuevo código OTP.
    4. Se establece un tiempo de expiración de 3 minutos.
    5. El nuevo OTP se guarda en la base de datos.

    Args:
        id_cliente (int): Identificador del cliente.

    Returns:
        str: Código OTP generado.
    """
    # Buscar OTP activos del cliente
    otps = OtpCodigo.query.filter_by(id_cliente=id_cliente, usado=False).all() 

    # Inactivar OTP anteriores
    for otp in otps: # se recorre la lista traida para inactivar los códigos activos
        otp.usado = True

    # Generar nuevo código OTP
    codigo_generado = generar_codigo()
    
    # Calcular tiempo de expiración
    expira = datetime.now(UTC) + timedelta(minutes=OTP_MINUTOS_EXPIRACION)
    
    # Crear nuevo registro OTP
    nuevo_otp = OtpCodigo(id_cliente=id_cliente, codigo=codigo_generado, expiracion=expira, usado=False) 

    # Guardar en base de datos
    db.session.add(nuevo_otp)
    db.session.commit()

    envio_sms(movil, codigo_generado)
    
    return codigo_generado

def verificar_otp(id_cliente, codigo, ahora=None):
    """
    Verifica si un código OTP ingresado por el cliente es válido.

    Orden de validación:
    1. Verificar si existe un OTP activo para el cliente.
    2. Validar que el código ingresado coincida con el registrado.
    3. Verificar si el código ha expirado.
    4. Si es válido, marcar el código como usado.

    Args:
        id_cliente (int): Identificador del cliente.
        codigo (str): Código OTP ingresado por el usuario.

    Returns:
        str: Resultado de la validación:
            - codigo_valido
            - codigo_invalido
            - codigo_expirado
            - codigo_no_existe
    """
    # Resolver dependencia de tiempo // esto se usa para testear
    if ahora is None:
        ahora = datetime.now(UTC).replace(tzinfo=None)

    # Buscar OTP activo del cliente
    otp = OtpCodigo.query.filter_by(id_cliente=id_cliente, usado=False).first()

    # No existe OTP activo
    if otp is None:
        return CODIGO_NO_EXISTE

    # El código ingresado no coincide
    if codigo != otp.codigo:
        return CODIGO_INVALIDO

    # El código expiró
    if ahora > otp.expiracion: 
        return CODIGO_EXPIRADO
    
    # El código es válido, se marca como usado
    otp.usado=True 
    db.session.commit()

    return CODIGO_VALIDO
