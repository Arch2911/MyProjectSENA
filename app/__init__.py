"""
app/__init__.py

Este módulo crea y configura la aplicación Flask utilizando el
patrón Application Factory. Aquí se inicializan las extensiones,
se carga la configuración del proyecto y se registran los modelos.
"""

from flask import Flask
from config import ProductionConfig
from .extensions import db, migrate
from .routes.auth import auth_bp
from .routes.orders import order_bp
from .routes.main import main_bp


def create_app(config_class=ProductionConfig):

    """
    Crea y configura una instancia de la aplicación Flask.

    Este método:
    1. Inicializa la aplicación Flask.
    2. Carga la configuración definida en la clase Config.
    3. Inicializa las extensiones del proyecto (base de datos,
        migraciones y gestión de autenticación).
    4. Registra los modelos de la aplicación.

    Returns:
        Flask: instancia configurada de la aplicación.
    """
    
    # Crear instancia de la aplicación Flask
    app = Flask(__name__)

    # Cargar configuración desde la clase Config
    app.config.from_object(config_class)

    # Inicializar extensiones con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(main_bp)

    # Importar modelos para que SQLAlchemy los registre
    from app import models

    return app