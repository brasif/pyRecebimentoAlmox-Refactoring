from flask import Blueprint

associacoes_bp = Blueprint('associacoes', __name__, url_prefix="/associacoes")


from .tabela_registros_por_responsavel_routes import *
from .tabela_registros_por_nota_fiscal_routes import *
from .tabela_notas_fiscais_por_filial_routes import *
from .tabela_responsaveis_por_filial_routes import *
from .tabela_filiais_por_responsavel import *
from .tabela_registros_por_responsavel_e_filial_routes import *
from .tabela_registros_atuais_por_filial_routes import *
from .tabela_todos_registros_por_filial_routes import *