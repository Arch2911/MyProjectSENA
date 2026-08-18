from flask import render_template, session, redirect, url_for

from . import main_bp

#Endpoint para cargar pagina inicial
@main_bp.route('/')
def home():
    return render_template('index.html')

#Endpoint para cargar la pagina de pedidos
@main_bp.route('/pedidos')
def pedidos():

    cedula = session.get('cedula')

    if 'cedula' not in session:
        return redirect(url_for('main.home'))
    
    return render_template('detalle_pedido.html')