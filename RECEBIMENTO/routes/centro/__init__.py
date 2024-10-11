from flask import Blueprint

centro_bp = Blueprint('centro', __name__, url_prefix="/centro")

from .criar_centro_routes import *
from .editar_centro_routes import *
