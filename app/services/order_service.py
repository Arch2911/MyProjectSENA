from ..extensions import db
from ..models.users import Cliente
from ..models.orders import Pedido

from ..services.constants import CLIENTE_NO_EXISTE



def obtener_pedido_cliente(cedula):

    cliente = Cliente.query.filter_by(cedula=cedula).first()

    if cliente is None:
        return CLIENTE_NO_EXISTE
    
    pedidos = Pedido.query.filter_by(id_cliente=cliente.id_cliente).all()


    lista_pedidos = []

    for pedido in pedidos:

        lista_pedidos.append({
            'numero_pedido': pedido.numero_pedido,
            'fecha_pedido': str(pedido.fecha_pedido),
            'total': pedido.total,
            'estado': pedido.estado.nombre_estado
            })

    return lista_pedidos
