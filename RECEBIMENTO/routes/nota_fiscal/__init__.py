from flask import Blueprint

nota_fiscal_bp = Blueprint('nota_fiscal', __name__, url_prefix="/nota_fiscal")


from .criar_nota_fiscal_routes import *
from .editar_nota_fiscal_routes import *
from .get_centros_por_filial import *
