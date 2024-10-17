from flask import Blueprint

gerenciamento_filial_bp = Blueprint('gerenciamento_filial', __name__, url_prefix="/gerenciamento_filial")


from .menu_filial_routes import *