from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object('config')
    
    # Inicializar SQLAlchemy
    db.init_app(app)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("Aplicación LIAN REPUESTOS iniciada")
    
    # Importar modelos para que SQLAlchemy los registre
    from app import models
    
    # Manejar errores de conexión BD
    try:
        with app.app_context():
            db.create_all()
            app.logger.info("Conexión a base de datos establecida correctamente")
    except Exception as e:
        app.logger.error(f"Error de conexión BD: {e}")
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.repuestos import repuestos_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(repuestos_bp)
    
    # Manejador de error 404
    @app.errorhandler(404)
    def not_found(e):
        from flask import url_for
        return render_template('errors/404.html'), 404
    
    return app
