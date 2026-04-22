from flask import render_template

from . import main_bp

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/pedidos')
def pedidos():
    return render_template('detalle_pedido.html')