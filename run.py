"""
run.py

Archivo principal para ejecutar la aplicación Flask.

Este módulo importa la función create_app desde el paquete app,
crea una instancia de la aplicación y la ejecuta en modo desarrollo
cuando el archivo se ejecuta directamente.
"""

from app import create_app

# Crear instancia de la aplicación Flask usando el patrón factory
app = create_app()

# Ejecutar el servidor solo si este archivo se ejecuta directamente
if __name__ == '__main__':
    app.run(debug=True)