from flask import request, jsonify, session
from app.services.order_service import obtener_pedido_cliente
from app.services.constants import CLIENTE_NO_EXISTE
from . import order_bp

# Endpoint de pedidos
@order_bp.route('/orders', methods = ['GET'])
def obtener_pedidos():

    # Obtiene la cédula desde la sesión
    cedula = session.get('cedula')

    # Si no hay sessión, cliente no autenticado
    if not cedula:
        return jsonify({
            'status': 'error',
            'error': 'no_autenticado'
        }), 401
    
    # Lógica para obtener pedidos
    resultado = obtener_pedido_cliente(cedula)

    if resultado == CLIENTE_NO_EXISTE:
        return jsonify({
            'status': 'error',
            'error': 'cliente_no_existe'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': resultado
    }), 200
