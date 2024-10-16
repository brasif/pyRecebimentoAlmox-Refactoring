from flask import Blueprint

visualizacao_bp = Blueprint('visualizacao', __name__, url_prefix="/visualizacao")


from .visualizacao_nota_fiscal_routes import *
from .visualizacao_responsavel_routes import *