from flask import Blueprint

ajax_get_bp = Blueprint('ajax_get', __name__, url_prefix="/ajax_get")


from .get_centros_por_filial import *
from .get_responsaveis_por_filial import *