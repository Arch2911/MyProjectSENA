def test_buscar_cliente_existente(cliente):

    from app.services import cliente_service
    from app.services.constants import OTP_ENVIADO

    # ACT
    resultado = cliente_service.buscar_cliente(cliente.cedula)

    # ASSERT
    assert resultado == OTP_ENVIADO

def test_buscar_cliente_inexistente(app):

    from app.services import cliente_service
    from app.services.constants import CLIENTE_NO_EXISTE

    # ACT
    resultado = cliente_service.buscar_cliente(cedula=123)

    # ASSERT
    assert resultado == CLIENTE_NO_EXISTE


def test_verificacion_cliente_existente_otp_valido(cliente):

    from app.services import cliente_service, otp_service
    from app.services.constants import CODIGO_VALIDO

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente, cliente.movil)

    # ACT
    resultado = cliente_service.verificacion_cliente_otp(cliente.cedula, codigo)

    # ASSERT
    assert resultado == CODIGO_VALIDO

def test_verificacion_cliente_inexistente(app):

    from app.services import cliente_service
    from app.services.constants import CLIENTE_NO_EXISTE

    # ARRANGE
    cedula = 123
    codigo = ""

    # ACT
    resultado = cliente_service.verificacion_cliente_otp(cedula, codigo)

    # ASSERT
    assert resultado == CLIENTE_NO_EXISTE

def test_verificacion_cliente_otp_invalido(cliente):

    from app.services import cliente_service, otp_service
    from app.services.constants import CODIGO_INVALIDO

    # ARRANGE
    otp_service.crear_otp(cliente.id_cliente, cliente.movil)
    codigo_invalido = 345234

    # ACT
    resultado = cliente_service.verificacion_cliente_otp(cliente.cedula, codigo_invalido)

    # ASSERT
    assert resultado == CODIGO_INVALIDO

def test_verificacion_cliente_otp_expirado(cliente, db_session):

    from app.services import cliente_service, otp_service
    from app.services.constants import CODIGO_EXPIRADO
    from app.models.otp_code import OtpCodigo
    from datetime import timedelta

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente, cliente.movil)
    otp_ex = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()
    otp_ex.expiracion = otp_ex.expiracion - timedelta(minutes=3)
    db_session.session.commit()

    # ACT
    resultado = cliente_service.verificacion_cliente_otp(cliente.cedula, codigo)

    # ASSERT
    assert resultado == CODIGO_EXPIRADO

def test_verificacion_cliente_otp_no_existe(cliente, db_session):

    from app.services import cliente_service, otp_service
    from app.services.constants import CODIGO_NO_EXISTE
    from app.models.otp_code import OtpCodigo

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente, cliente.movil)
    otp = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente, usado=False).first()
    otp.usado = True
    db_session.session.commit()

    # ACT
    resultado = cliente_service.verificacion_cliente_otp(cliente.cedula, codigo)

    # ASSERT
    assert resultado == CODIGO_NO_EXISTE