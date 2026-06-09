from flask import render_template

from . import main_bp

#Endpoint para cargar pagina inicial
@main_bp.route('/')
def home():
    return render_template('index.html')

#Endpoint para cargar la pagina de pedidos
@main_bp.route('/pedidos')
def pedidos():
    return render_template('detalle_pedido.html')