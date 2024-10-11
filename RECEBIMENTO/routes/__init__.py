from .menu_routes import menu_bp
from .autenticacao import autenticacao_bp
from .centro import centro_bp

def register_blueprint(app):
    app.register_blueprint(menu_bp)
    app.register_blueprint(autenticacao_bp)
    app.register_blueprint(centro_bp)
