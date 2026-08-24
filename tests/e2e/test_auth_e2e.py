

def test_autenticacion_cliente_existente_otp_valido(auth_page, app, live_server, cliente):

    from app.models.otp_code import OtpCodigo

    # live_server contiene la URL "http://127.0.0.1:5000"
    auth_page.abrir_pagina(live_server)

    auth_page.consultar(cliente.cedula)

    auth_page.texto_visible("SMS enviado con exito")

    with app.app_context():
        otp_registro = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente, usado=False).first()
        codigo = otp_registro.codigo

    auth_page.verificar_otp(codigo)

    auth_page.texto_visible("Verificación exitosa")


def test_autenticacion_cliente_inexistente(auth_page, live_server):

    auth_page.abrir_pagina(live_server)

    auth_page.consultar(124)

    auth_page.texto_visible("Cliente no existe")


def test_autenticacion_cliente_existente_otp_invalido(auth_page, live_server, cliente):

    auth_page.abrir_pagina(live_server)

    auth_page.consultar(cliente.cedula)

    codigo = "123556" # código invalido

    auth_page.verificar_otp(codigo)

    auth_page.texto_visible("El código ingresado es incorrecto")


def test_autenticacion_cliente_existente_otp_expirado(auth_page, app, live_server, cliente, db_session):

    from app.models.otp_code import OtpCodigo
    from datetime import timedelta

    auth_page.abrir_pagina(live_server)

    auth_page.consultar(cliente.cedula)

    with app.app_context():

        otp_registro = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente, usado=False).first()
        codigo = otp_registro.codigo
        otp_registro.expiracion = otp_registro.expiracion - timedelta(minutes=4)

        db_session.session.commit()
        db_session.session.remove()

    auth_page.verificar_otp(codigo)

    auth_page.texto_visible("El código ha expirado")

def test_cliente_autenticado_con_pedido(page_autenticada, auth_page, live_server):

    page_autenticada.goto(f"{live_server}/pedidos")

    auth_page.texto_visible("Lista de pedidos")

    page_autenticada.get_by_role("button", name="Ver").click()

    auth_page.texto_visible("Productos del pedido")

    page_autenticada.get_by_role("button", name="Cerrar").click()

    page_autenticada.get_by_role("link", name="Logout").click()



