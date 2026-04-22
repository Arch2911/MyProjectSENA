"""
extensions.py

Este módulo inicializa las extensiones utilizadas por la aplicación Flask.
Las extensiones se crean aquí para ser importadas y registradas posteriormente
dentro de la función create_app() siguiendo el patrón Application Factory.
"""

from flask_sqlalchemy import SQLAlchemy # permite conectar Flask con una base de datos usando el ORM(Object Relational Mapper) SQLAlchemy.
from flask_migrate import Migrate
from flask_login import LoginManager

# Instancia de SQLAlchemy para gestionar la base de datos
db = SQLAlchemy()

# Instancia de Migrate para manejar migraciones de la base de datos
migrate = Migrate()

# Gestor de autenticación de usuarios
login_manager = LoginManager()

# Ruta a la que se redirige cuando un usuario no autenticado
# intenta acceder a una vista protegida
login_manager.login_view = 'index'