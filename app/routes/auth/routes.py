
from flask import request, jsonify, session
from app.services.cliente_service import buscar_cliente, verificacion_cliente_otp
from app.services.constants import CLIENTE_NO_EXISTE, OTP_ENVIADO, CODIGO_INVALIDO, CODIGO_EXPIRADO, CODIGO_VALIDO

from . import auth_bp


# Endpoint para consultar cliente con cédula.
@auth_bp.route('/auth/login', methods = ['POST'])
def buscar_cedula():

    data = request.get_json()

    if not data:
        return jsonify({
            'status': 'error',
            'error': 'json_requerido'
        }), 400
    
    # Obtener cédula
    cedula = data.get('cedula')

    if not cedula:
        return jsonify({
            'status': 'error',
            'error': 'cedula_requerida'
        }), 400
    
    # Lógica (envio de OTP)
    resultado = buscar_cliente(cedula)

    if resultado == CLIENTE_NO_EXISTE:
        return jsonify({
            'status': 'error',
            'error': 'cliente_no_existe'
        }), 404

    
    if resultado == OTP_ENVIADO:

        session['cedula_temporal'] = cedula

        return jsonify({
            'status': 'success'
        }), 200
    
    return jsonify({
        'status': 'error',
        'error': 'error_interno'
    }), 500
    
# Endpoint para verificar el código OTP.
@auth_bp.route('/auth/verify', methods = ['POST'])
def verificar_otp():

    data = request.get_json()

    if not data:
        return jsonify({
            'status': 'error',
            'error': 'json_requerido'
        }), 400
    
    cedula = session.get('cedula_temporal')
    if not cedula:
        return jsonify({
            'status': 'error',
            'error': 'sesion_invalida'
        }), 401
    
    codigo = data.get('codigo')
    if not codigo:
        return jsonify({
            'status': 'error',
            'error': 'codigo_requerido'
        }), 400
    
    resultado = verificacion_cliente_otp(cedula, codigo)

    if resultado == CLIENTE_NO_EXISTE:
        return jsonify({
            'status': 'error',
            'error': 'cliente_no_existe'
        }), 404
    
    if resultado == CODIGO_INVALIDO:
        return jsonify({
            'status': 'error',
            'error': 'codigo_invalido'
        }), 401
    
    if resultado == CODIGO_EXPIRADO:
        return jsonify({
            'status': 'error',
            'error': 'codigo_expirado'
        }), 410

    
    if resultado == CODIGO_VALIDO:

        session.pop('cedula_temporal', None) # se elimina temporal
        session['cedula'] = cedula # se crea session real ya verificada

        return jsonify({
            'status': 'success'
        }), 200
    
    return jsonify({
        'status': 'error',
        'error': 'error_interno'
    }), 500

@auth_bp.route('/auth/logout', methods = ['POST'])
def logout():

    session.pop('cedula', None)

    return jsonify({
        'status': 'success',
    }), 200