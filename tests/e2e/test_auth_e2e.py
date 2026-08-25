

def test_autenticacion_cliente_existente_otp_valido(auth_page, base, app, live_server, cliente):

    from app.models.otp_code import OtpCodigo

    # live_server contiene la URL "http://127.0.0.1:5000"
    auth_page.abrir_pagina(live_server)

    auth_page.consultar(cliente.cedula)

    base.texto_visible("SMS enviado con exito")

    with app.app_context():
        otp_registro = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente, usado=False).first()
        codigo = otp_registro.codigo

    auth_page.verificar_otp(codigo)

    base.texto_visible("Verificación exitosa")


def test_autenticacion_cliente_inexistente(auth_page, base, live_server):

    auth_page.abrir_pagina(live_server)

    auth_page.consultar(124)

    base.texto_visible("Cliente no existe")


def test_autenticacion_cliente_existente_otp_invalido(auth_page, base, live_server, cliente):

    auth_page.abrir_pagina(live_server)

    auth_page.consultar(cliente.cedula)

    codigo = "123556" # código invalido

    auth_page.verificar_otp(codigo)

    base.texto_visible("El código ingresado es incorrecto")


def test_autenticacion_cliente_existente_otp_expirado(auth_page, base, app, live_server, cliente, db_session):

    from app.models.otp_code import OtpCodigo
    from datetime import timedelta

    auth_page.abrir_pagina(live_server)

    auth_page.consultar(cliente.cedula)

    with app.app_context():

        otp_registro = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente, usado=False).first()
        codigo = otp_registro.codigo
        otp_registro.expiracion = otp_registro.expiracion - timedelta(minutes=4)

        db_session.commit()

    auth_page.verificar_otp(codigo)

    base.texto_visible("El código ha expirado")

def test_cliente_autenticado_con_pedido(order_page, base , detalle_pedido):


    base.texto_visible("Lista de pedidos")

    order_page.ver_detalles()

    base.texto_visible("Productos del pedido")

    order_page.cerrar_detalles()

    order_page.cerrar_sesion()

def test_cliente_autenticado_sin_pedido(order_page, base):

    base.texto_visible("Lista de pedidos")

    base.texto_visible("No tienes pedidos registrados")

    order_page.cerrar_sesion()



