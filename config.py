"""
config.py

Este módulo contiene la configuración principal de la aplicación Flask.
Carga variables de entorno y define la clase Config que centraliza
los parámetros de configuración del proyecto.

Se utilizan variables almacenadas en un archivo .env para mantener
segura la información sensible como claves secretas y conexión a base de datos.
"""

from dotenv import load_dotenv 
from pathlib import Path #pathlib → módulo para manejar rutas, Path → clase que representa una ruta del sistema de archivos
import os

load_dotenv()

# Ruta absoluta del directorio donde se encuentra este archivo.
# Se usa como referencia para construir rutas dentro del proyecto.
BASE_DIR = Path(__file__).resolve().parent

class Config:
    """
    Clase de configuración principal para la aplicación Flask.

    Atributos:
        SECRET_KEY (str): clave secreta utilizada por Flask para sesiones y seguridad.
        SQLALCHEMY_DATABASE_URI (str): cadena de conexión a la base de datos.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): desactiva el seguimiento de cambios o actualizaciones realizadas
        en SQLAlchemy para mejorar el rendimiento y no ocupar más memoria.
    """
    # Clave secreta obtenida desde variables de entorno (.env)
    SECRET_KEY = os.getenv('SECRET_KEY')



    # Desactiva notificaciones innecesarias de SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):

    # URI de conexión a la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE')

class TestingConfig(Config):

    TESTING = True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'