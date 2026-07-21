import pytest

from app import create_app
from app.extensions import db
from config import TestingConfig

@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():

        from app.models.users import Cliente
        from app.models.orders import Pedido
        from app.models.otp_code import OtpCodigo

        db.create_all()
        yield app
        db.drop_all()

"""
@pytest.fixture
def db_session(app):
    return db
"""

@pytest.fixture
def cliente(app):
    from app.models.users import Cliente

    cliente = Cliente(cedula='123',nombre='Juan', apellido='Contrera', correo='notiene@notiene.com', movil='3001234567')
    db.session.add(cliente)
    db.session.commit()

    return cliente

@pytest.fixture
def estado(app):
    from app.models.orders import Estado
    
    estado = Estado(nombre_estado='En camino')
    db.session.add(estado)
    db.session.commit()

    return estado

@pytest.fixture
def pedido(app, cliente, estado):
    from app.models.orders import Pedido
    from datetime import datetime, UTC

    pedido = Pedido(numero_pedido='123-abc', fecha_pedido=datetime.now(UTC), total='50000', id_cliente=cliente.id_cliente, estado_actual_id=estado.id_estado)
    db.session.add(pedido)
    db.session.commit()

    return pedido


