def test_obtener_pedido_cliente_existente_con_pedido(cliente, pedido, detalle_pedido):

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

    assert 'detalles' in pedido_obtenido
    assert isinstance(pedido_obtenido['detalles'], list)
    assert len(pedido_obtenido['detalles']) == 1


    detalle_obtenido = pedido_obtenido['detalles'][0]
    assert detalle_obtenido['nombre_producto'] == detalle_pedido.producto.nombre
    assert detalle_obtenido['cantidad'] == detalle_pedido.cantidad
    assert detalle_obtenido['precio_unitario'] == detalle_pedido.precio_unitario
    assert detalle_obtenido['subtotal'] == detalle_pedido.subtotal

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