from .menu_routes import menu_bp
from .autenticacao import autenticacao_bp
from .responsavel import responsavel_bp
from .responsavel_filial import responsavel_filial_bp
from .nota_fiscal_e_recebimento import nota_fiscal_bp
from .mudar_status import mudar_status_bp
from .tabelas import tabela_bp

def register_blueprint(app):
    app.register_blueprint(menu_bp)
    app.register_blueprint(autenticacao_bp)
    app.register_blueprint(responsavel_bp)
    app.register_blueprint(responsavel_filial_bp)
    app.register_blueprint(nota_fiscal_bp)
    app.register_blueprint(mudar_status_bp)
    app.register_blueprint(tabela_bp)