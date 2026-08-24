import pytest

from app import create_app
from app.extensions import db
from config import TestingConfig

# Fixture para crear el contexto de la aplicación y la base de datos de pruebas.
@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():

        from app.models.users import Cliente
        from app.models.orders import Pedido
        from app.models.otp_code import OtpCodigo

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# Fixture para acceder a la sesión de la base de datos durante las pruebas.
@pytest.fixture
def db_session(app):
    yield db

# Fixture para simular cliente registrado en bd durante las pruebas.
@pytest.fixture
def cliente(app):
    from app.models.users import Cliente

    cliente = Cliente(cedula='123',nombre='Juan', apellido='Contrera', correo='notiene@notiene.com', movil='3001234567')
    db.session.add(cliente)
    db.session.commit()

    yield cliente

# Fixture para simular estado registrado en bd durante las pruebas.
@pytest.fixture
def estado(app):
    from app.models.orders import Estado
    
    estado = Estado(nombre_estado='En camino')
    db.session.add(estado)
    db.session.commit()

    yield estado

# Fixture para simular producto registrado en BD
@pytest.fixture
def producto(app):
    from app.models.orders import Producto

    prod = Producto(
        nombre='Laptop Gamer',
        precio=50000
    )
    db.session.add(prod)
    db.session.commit()
    yield prod

# Fixture para simular pedido registrado en bd durante las pruebas.
@pytest.fixture
def pedido(app, cliente, estado):
    from app.models.orders import Pedido
    from datetime import datetime, UTC

    pedido = Pedido(numero_pedido='123-abc', fecha_pedido=datetime.now(UTC), total='50000', id_cliente=cliente.id_cliente, estado_actual_id=estado.id_estado)
    db.session.add(pedido)
    db.session.commit()

    yield pedido

# Fixture para vincular el pedido con el producto a través de DetallePedido
@pytest.fixture
def detalle_pedido(app, pedido, producto):
    from app.models.orders import DetallePedido

    detalle = DetallePedido(
        id_pedido=pedido.id_pedido,
        id_producto=producto.id_producto,
        cantidad=1,
        precio_unitario=50000,
        subtotal=50000
    )
    db.session.add(detalle)
    db.session.commit()
    yield detalle

# Fixture para simular peticiones HTTP a la aplicación durante las pruebas.
@pytest.fixture
def peticiones(app):
    yield app.test_client()

# Fixture para simular peticiones HTTP, con session activa durante las pruebas a ejecutar.
@pytest.fixture
def peticiones_autenticadas(cliente, peticiones):
    with peticiones.session_transaction() as session:
        session["cedula_temporal"] = cliente.cedula
    yield peticiones


@pytest.fixture
def live_server(app):

    import time
    import threading
    from werkzeug.serving import make_server

    server = make_server('127.0.0.1', 5000, app)

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    time.sleep(0.5)

    yield 'http://127.0.0.1:5000'

    server.shutdown()

import re
from playwright.sync_api import Page
from tests.e2e.page.page_auth import Autenticacion

@pytest.fixture
def auth_page(page: Page):
    yield Autenticacion(page)



@pytest.fixture
def page_autenticada(page: Page, app, live_server, cliente, pedido, detalle_pedido):

    from app.models.otp_code import OtpCodigo

    page.goto(live_server)

    page.get_by_placeholder("Ingrese su número de identificación").fill(str(cliente.cedula))

    page.get_by_role("button", name="Continuar").click()

    with app.app_context():
        otp_registro = OtpCodigo.query.filter_by(id_cliente=cliente.id_cliente, usado=False).first()
        codigo = otp_registro.codigo

    page.locator(".code-input").first.click()

    page.keyboard.type(codigo)

    page.get_by_role("button", name="Verificar").click()

    yield page
