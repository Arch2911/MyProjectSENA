def test_obtener_pedido_cliente_existente_con_pedido(cliente, pedido):

    from app.services import order_service

    # ARRANGE

    # ACT
    resultado = order_service.obtener_pedido_cliente(cliente.cedula)

    # ASSERT
    assert resultado
    assert isinstance(resultado, list)
    assert len(resultado) == 1

    pedido_obtenido = resultado[0]
    assert pedido_obtenido['numero_pedido'] == pedido.numero_pedido
    assert str(pedido_obtenido['fecha_pedido']) == str(pedido.fecha_pedido)
    assert pedido_obtenido['total'] == pedido.total
    assert (pedido_obtenido['estado']) == pedido.estado.nombre_estado

def test_obtener_pedido_cliente_existente_sin_pedido(cliente):

    from app.services import order_service

    # ARRANGE

    # ACT
    resultado = order_service.obtener_pedido_cliente(cliente.cedula)

    # ASSERT
    assert resultado == []

def test_obtener_pedido_cliente_inexistente(app):

    from app.services import order_service
    from app.services.constants import CLIENTE_NO_EXISTE

    # ARRANGE

    # ACT
    resultado = order_service.obtener_pedido_cliente(cedula=123)

    # ASSERT
    assert resultado == CLIENTE_NO_EXISTE