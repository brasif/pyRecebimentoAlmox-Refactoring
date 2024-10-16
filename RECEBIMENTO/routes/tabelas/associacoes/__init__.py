from flask import Blueprint

associacoes_bp = Blueprint('associacoes', __name__, url_prefix="/associacoes")


from .tabela_registros_por_responsavel_routes import *
from .tabela_registros_por_nota_fiscal_routes import *