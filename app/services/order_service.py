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

        detalles_lista = []

        for detalle in pedido.detalles:
            detalles_lista.append({
                'nombre_producto': detalle.producto.nombre if detalle.producto else 'Producto',
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'subtotal': detalle.subtotal
            })

        lista_pedidos.append({
            'id': pedido.id_pedido,
            'numero_pedido': pedido.numero_pedido,
            'fecha_pedido': str(pedido.fecha_pedido),
            'total': pedido.total,
            'estado': pedido.estado.nombre_estado,
            'detalles': detalles_lista
            })

    return lista_pedidos
