def test_crear_otp(db_session, cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    



    codigo = otp_service.crear_otp(cliente.id_cliente)

    assert codigo is not None

    assert len(codigo) == 6

    otp_db = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    assert otp_db is not None

    assert otp_db.codigo == codigo

    assert otp_db.usado is False

    assert otp_db.expiracion is not None

def test_crear_otp_cambio_de_estado(db_session, cliente):
    
    from app.models.otp_code import OtpCodigo
    from app.services import otp_service

    otp1 = otp_service.crear_otp(cliente.id_cliente)

    otp2 = otp_service.crear_otp(cliente.id_cliente)

    otp_bd = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).all()

    for otp in otp_bd:

        if otp.codigo == otp1:
            otp1_bd = otp

        if otp.codigo == otp2:
            otp2_bd = otp

    assert otp1_bd is not None
    assert otp2_bd is not None

    assert otp1_bd.usado is True
    assert otp2_bd.usado is False



def test_verificar_otp_valido(db_session, cliente):

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

def test_verificar_otp_correcto_pero_usado(db_session, cliente):

    from app.services import otp_service
    from app.models.otp_code import OtpCodigo
    from app.services.constants import CODIGO_NO_EXISTE

    codigo = otp_service.crear_otp(cliente.id_cliente)

    otp = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    assert otp.codigo == codigo

    ingreso_codigo1 = otp_service.verificar_otp(cliente.id_cliente, codigo)

    ingreso_codigo2 = otp_service.verificar_otp(cliente.id_cliente, codigo)

    assert ingreso_codigo2 == CODIGO_NO_EXISTE

def test_verificar_otp_invalido(db_session, cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_INVALIDO

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente)

    # ACT
    codigo_mal_ingresado = '123567'

    if codigo == codigo_mal_ingresado:
        codigo_mal_ingresado = '765321'

    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo_mal_ingresado)

    # ASSERT (resultado)
    assert resultado == CODIGO_INVALIDO


def test_verificar_otp_expirado(db_session, cliente):

    from datetime import timedelta
    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_EXPIRADO

    # ARRANGE
    codigo = otp_service.crear_otp(cliente.id_cliente)

    otp_db = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

    ahora = otp_db.expiracion + timedelta(seconds=1)

    ahora = ahora.replace(tzinfo=None)

    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo, ahora=ahora)

    assert resultado == CODIGO_EXPIRADO

def test_verificar_otp_no_existe(db_session, cliente):

    from app.models.otp_code import OtpCodigo
    from app.services import otp_service
    from app.services.constants import CODIGO_NO_EXISTE

    #ARRANGE
    
    # ACT
    codigo = '123456' # código ingresado por el cliente.
    resultado = otp_service.verificar_otp(cliente.id_cliente, codigo)

    # ASSERT
    assert resultado == CODIGO_NO_EXISTE


def test_buscar_pedidos_cliente_no_existe(db_session, cliente):

    from app.services import order_service
    from app.services.constants import CLIENTE_NO_EXISTE

    cedula = '124'

    resultado = order_service.buscar_pedidos_cliente(cedula)

    assert resultado == CLIENTE_NO_EXISTE

def test_buscar_pedidos_cliente_sin_pedido(db_session, cliente):


    from app.services import order_service
    from app.services.constants import CLIENTE_SIN_PEDIDOS

    cedula = '123'

    resultado = order_service.buscar_pedidos_cliente(cedula)

    assert resultado == CLIENTE_SIN_PEDIDOS

def test_buscar_pedidos_cliente_exitoso(db_session, cliente, pedido):

    from app.services import order_service
    from app.services.constants import OTP_ENVIADO
    from unittest.mock import patch
    from app.models.otp_code import OtpCodigo

    with patch('app.services.sms_service.envio_sms') as mock_sms:

        #ACT
        resultado = order_service.buscar_pedidos_cliente('123')

        #ASSERT retorno
        assert resultado == OTP_ENVIADO

        # ASSERT se valida que se haya creado el código en BD
        otp = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()
        assert otp is not None

        #ASSERT
        mock_sms.assert_called_once()

def test_buscar_pedidos_cliente_sms_enviado(db_session, cliente, pedido):

    from app.services import order_service
    from unittest.mock import patch
    from app.models.otp_code import OtpCodigo

    with patch('app.services.sms_service.envio_sms') as mock_sms:
        
        #Act
        order_service.buscar_pedidos_cliente(cliente.cedula)

        # Obtener OTP generado en BD
        otp = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente).first()

        # Assert: SMS enviado con datos correctos
        mock_sms.assert_called_once_with(cliente.movil, otp.codigo)

def test_verificacion_total_mostrar_pedidos_cliente_no_existe(db_session):

    from app.services import order_service
    from app.services.constants import CLIENTE_NO_EXISTE

    resultado = order_service.verificacion_total_mostrar_pedidos('124', '000000')

    assert resultado == CLIENTE_NO_EXISTE

def test_verificacion_total_mostrar_pedidos_otp_invalido(db_session, cliente):

    from app.services import order_service
    from unittest.mock import patch
    from app.services.constants import CODIGO_INVALIDO

    with patch('app.services.otp_service.verificar_otp') as mock_otp, \
        patch('app.services.order_service.Pedido.query.filter_by') as mock_pedido:

        mock_otp.return_value = CODIGO_INVALIDO

        resultado = order_service.verificacion_total_mostrar_pedidos(cliente.cedula, '000000')

        assert resultado == CODIGO_INVALIDO

        mock_pedido.assert_not_called()

def test_verificacion_total_mostrar_pedidos_cliente_sin_pedidos(db_session, cliente):

    from app.services import order_service
    from unittest.mock import patch
    from app.services.constants import CLIENTE_SIN_PEDIDOS, CODIGO_VALIDO

    with patch('app.services.otp_service.verificar_otp') as mock_otp:

        mock_otp.return_value = CODIGO_VALIDO

        resultado = order_service.verificacion_total_mostrar_pedidos(cliente.cedula, '000000')

    assert resultado == CLIENTE_SIN_PEDIDOS

def test_verificacion_total_mostrar_pedidos_ok(db_session, cliente, pedido):

    from app.services import order_service
    from unittest.mock import patch
    from app.services.constants import CODIGO_VALIDO



    with patch('app.services.otp_service.verificar_otp') as mock_otp:
        mock_otp.return_value = CODIGO_VALIDO

        resultado = order_service.verificacion_total_mostrar_pedidos('123', '000000')

    # Se valida que sea lista
    assert isinstance(resultado, list)

    # se valida que haya al menos 1 pedido
    assert len(resultado) == 1

    pedido_resultado = resultado[0]

    # Se valida la estructura completa
    assert set(pedido_resultado.keys()) == {
        'numero_pedido',
        'fecha_pedido',
        'total',
        'estado'
    }

    # validar contenido real
    assert pedido_resultado['numero_pedido'] == pedido.numero_pedido
    assert pedido_resultado['total'] == pedido.total 





