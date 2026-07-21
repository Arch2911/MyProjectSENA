

def test_generar_codigo():

    from app.services import otp_service

    codigo = otp_service.generar_codigo()

    assert codigo is not None

    assert len(codigo) == 6

    assert codigo.isdigit()

def test_crear_otp(cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from unittest.mock import patch


        # ARRANGE
    with patch('app.services.otp_service.envio_sms') as mock_sms:
        
        #ACT
        codigo = otp_service.crear_otp(cliente.id_cliente, cliente.movil)

        # ASSERT
        otp_db = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

        assert otp_db is not None

        assert otp_db.codigo == codigo

        assert otp_db.usado is False

        assert otp_db.expiracion is not None

        assert otp_db.codigo is not None

        mock_sms.assert_called_once_with(cliente.movil, codigo)

def test_crear_otp_cambio_de_estado(cliente):
    
    from app.models.otp_code import OtpCodigo
    from app.services import otp_service

    otp1 = otp_service.crear_otp(cliente.id_cliente)

    otp2 = otp_service.crear_otp(cliente.id_cliente)

    otp_db = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).all()

    for otp in otp_db:

        if otp.codigo == otp1:
            otp1_db = otp

        if otp.codigo == otp2:
            otp2_db = otp

    assert otp1_db is not None
    assert otp2_db is not None

    assert otp1_db.usado is True
    assert otp2_db.usado is False



def test_verificar_otp_valido(cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_VALIDO

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente)

    otp_db = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    assert otp_db.usado is False

    #ACT
    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo)

    # ASSERT (resultado)
    assert resultado == CODIGO_VALIDO

    # ASSERT (Se consulta nuevamente el estado del código actualizado en BD)
    otp_actualizado = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()
    assert otp_actualizado.usado is True

def test_verificar_otp_valido_pero_usado(cliente):

    from app.services import otp_service
    from app.models.otp_code import OtpCodigo
    from app.services.constants import CODIGO_NO_EXISTE

    codigo = otp_service.crear_otp(cliente.id_cliente)

    otp = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    assert otp.codigo == codigo

    ingreso_codigo1 = otp_service.verificar_otp(cliente.id_cliente, codigo)

    otp = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    assert otp.usado is True

    ingreso_codigo2 = otp_service.verificar_otp(cliente.id_cliente, codigo)

    assert ingreso_codigo2 == CODIGO_NO_EXISTE

def test_verificar_otp_invalido(cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_INVALIDO

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente, cliente.movil)

    # ACT
    codigo_mal_ingresado = '123567'

    if codigo == codigo_mal_ingresado:
        codigo_mal_ingresado = '765321'

    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo_mal_ingresado)

    # ASSERT (resultado)
    assert resultado == CODIGO_INVALIDO


def test_verificar_otp_expirado(cliente):

    from datetime import timedelta
    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_EXPIRADO

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente, cliente.movil)

    otp_db = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    ahora = otp_db.expiracion + timedelta(seconds=1)

    ahora = ahora.replace(tzinfo=None)

    # Act
    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo, ahora=ahora)

    # Assert
    assert resultado == CODIGO_EXPIRADO


def test_verificar_otp_no_existe(cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_NO_EXISTE

    #ARRANGE
    codigo = '123456' # código ingresado por el cliente.
    
    # ACT
    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo)

    # ASSERT
    assert resultado == CODIGO_NO_EXISTE
