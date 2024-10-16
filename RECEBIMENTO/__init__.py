# ========== IMPORTAÇÕES ==========
from flask import Flask  # Flask
from flask_sqlalchemy import SQLAlchemy  # Gerenciamento do Banco de dados
from flask_login import LoginManager  # Gerenciamento do Login
from flask_wtf.csrf import CSRFProtect  # Proteção contra ataques CSRF

# Configurações de ambiente
from app_config import Config


# ========== INICIALIZAÇÃO DE EXTENSÕES ==========
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


# ========== APP ==========
def criacao_app():
    # Configura a pasta static para importações como CSS e JS
    app = Flask(__name__, static_folder='./static')
    # Configuração do app
    app.config.from_object(Config)

    # inicialização de extensões Flask com o app
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Importação dos models após a inicialização do app
    with app.app_context():
        from RECEBIMENTO.models import Responsavel, Filiais  # Tabela com os usuários do sistema e enum Filiais

    # Carrega as informações do usuário através do id
    @login_manager.user_loader
    def load_user(user_id):
        return Responsavel.query.get(int(user_id))

    # Registrar blueprints
    from RECEBIMENTO.routes import register_blueprint
    register_blueprint(app)

    # Adiciona o Enum Filiais em todos os templates para dropdown em navbar (base.html)
    @app.context_processor
    def inject_filiais():
        return dict(Filiais=Filiais)

    return app


# Criação do objeto app
app = criacao_app()
