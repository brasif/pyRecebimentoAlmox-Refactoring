from flask import Blueprint

responsavel_filial_bp = Blueprint('responsavel_filial', __name__, url_prefix="/responsavel_filial")

from .criar_responsavel_filial_routes import *
from .editar_responsavel_filial_routes import *
from .excluir_responsavel_filial_routes import *