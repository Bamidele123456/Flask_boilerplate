from flask import Blueprint
from .auth import auth_bp
from .main import main_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
