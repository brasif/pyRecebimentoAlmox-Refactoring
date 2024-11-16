# ========== IMPORTAÇÕES ==========
import logging  # Adicionado para o log
from logging.handlers import RotatingFileHandler  # Log com rotação de arquivos
import os  # Importado para manipular o caminho do log
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

    # Configuração de log
    configurar_log(app)

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


# ========== LOG ==========
def configurar_log(app):
    # Define o diretório de logs
    log_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(log_dir):  # Cria a pasta se não existir
        os.makedirs(log_dir)
    
    # Define o arquivo de log dentro do diretório
    log_file = os.path.join(log_dir, "app.log")

    # Configura o manipulador de log com rotação
    handler = RotatingFileHandler(
        log_file, maxBytes=100000, backupCount=10
    )  # Rotação do log
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )  # Formato do log
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Aplicação iniciada com sucesso.")  # Mensagem inicial


# Criação do objeto app
app = criacao_app()
