from flask import Blueprint

tabela_bp = Blueprint('tabela', __name__, url_prefix="/tabela")


from .tabela_responsaveis_routes import *
from .tabela_responsaveis_filial_routes import *
from .tabela_notas_fiscais_routes import *