
def test_buscar_pedidos_cliente_no_existe(cliente):

    from app.services import order_service
    from app.services.constants import CLIENTE_NO_EXISTE

    # ARRANGE
    cedula = '124'

    # ACT
    resultado = order_service.obtener_pedido_cliente(cedula)

    # ASSERT
    assert resultado == CLIENTE_NO_EXISTE

def test_buscar_pedidos_cliente_sin_pedido(cliente):


    from app.services import order_service
    from app.services.constants import CLIENTE_SIN_PEDIDOS

    # ARRANGE
    cedula = '123'

    # ACT
    resultado = order_service.obtener_pedido_cliente(cedula)

    # ASSERT
    assert resultado == CLIENTE_SIN_PEDIDOS

def test_buscar_pedidos_cliente_exitoso(cliente, pedido):

    from app.services import order_service

    #ACT
    resultado = order_service.obtener_pedido_cliente(cliente.cedula)

    #ASSERT
    assert isinstance(resultado, list)
    assert len(resultado) == 1

    primer_pedido = resultado[0]
    assert primer_pedido['numero_pedido'] == pedido.numero_pedido
    assert primer_pedido['total'] == pedido.total
    assert primer_pedido['estado'] == pedido.estado.nombre_estado
    assert isinstance(primer_pedido['fecha_pedido'], str)


def test_verificacion_total_mostrar_pedidos_cliente_no_existe():

    from app.services import order_service
    from app.services.constants import CLIENTE_NO_EXISTE

    resultado = order_service.verificacion_total_mostrar_pedidos('124', '000000')

    assert resultado == CLIENTE_NO_EXISTE

def test_verificacion_total_mostrar_pedidos_otp_invalido(cliente):

    from app.services import order_service
    from unittest.mock import patch
    from app.services.constants import CODIGO_INVALIDO

    with patch('app.services.otp_service.verificar_otp') as mock_otp, \
        patch('app.services.order_service.Pedido.query.filter_by') as mock_pedido:

        mock_otp.return_value = CODIGO_INVALIDO

        resultado = order_service.verificacion_total_mostrar_pedidos(cliente.cedula, '000000')

        assert resultado == CODIGO_INVALIDO

        mock_pedido.assert_not_called()

def test_verificacion_total_mostrar_pedidos_cliente_sin_pedidos(cliente):

    from app.services import order_service
    from unittest.mock import patch
    from app.services.constants import CLIENTE_SIN_PEDIDOS, CODIGO_VALIDO

    with patch('app.services.otp_service.verificar_otp') as mock_otp:

        mock_otp.return_value = CODIGO_VALIDO

        resultado = order_service.verificacion_total_mostrar_pedidos(cliente.cedula, '000000')

    assert resultado == CLIENTE_SIN_PEDIDOS

def test_verificacion_total_mostrar_pedidos_ok(cliente, pedido):

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





